"""Shiny for Python industrial data augmentation platform (Core API)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from shiny import App, reactive, render, ui

from modules.augmentation_config import AugmentationConfigModule
from modules.augmentation_run import AugmentationRunModule
from modules.export import ExportModule
from modules.harmonization import HarmonizationModule
from modules.merge_build import MergeBuildModule
from modules.package_ingestion import PackageIngestionModule
from modules.profiling import ProfilingModule
from modules.project_manager import ProjectManager
from modules.registry import Registry
from modules.report import ReportModule
from modules.schema_validation import SchemaValidationModule
from services.ingestion_service import IngestionService
from services.lineage_service import LineageService
from utils.constants import FINAL_DIR, MASTER_DATASET_NAME, RAW_DIR

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h4("Projekt"),
        ui.input_text("project_name", "Projektname", "industrial_timeseries_platform"),
        ui.input_text("owner", "Owner", "data-team"),
        ui.input_action_button("init_project", "Projekt erstellen/laden"),
        ui.hr(),
        ui.h4("Upload"),
        ui.input_text("package_dir", "Pfad zum Paketordner", "sample_data/package_001"),
        ui.input_action_button("ingest_btn", "Paket importieren"),
        ui.input_action_button("ingest_batch_btn", "Beide Sample-Pakete importieren"),
        ui.hr(),
        ui.h4("Augmentation Config"),
        ui.input_checkbox_group(
            "aug_methods",
            "Methoden",
            {
                "jitter": "jitter",
                "scaling": "scaling",
                "noise": "noise",
                "event_shift": "event shift",
                "severity_scaling": "severity scaling",
                "actuator_delay": "actuator delay",
            },
            selected=["jitter", "noise"],
        ),
        ui.input_action_button("augment_btn", "Augmentation starten"),
        ui.input_action_button("build_btn", "Master Dataset bauen"),
        ui.input_action_button("export_btn", "Export"),
    ),
    ui.navset_tab(
        ui.nav_panel("Input", ui.output_text_verbatim("input_status")),
        ui.nav_panel("Registry", ui.output_data_frame("registry_table")),
        ui.nav_panel("Data Quality", ui.output_text_verbatim("quality_txt")),
        ui.nav_panel("Visualization", ui.output_plot("plot_signal"), ui.output_plot("plot_events")),
        ui.nav_panel("Harmonized Data", ui.output_data_frame("harmonized_table")),
        ui.nav_panel("Augmentation", ui.output_text_verbatim("aug_txt")),
        ui.nav_panel("Build Dataset", ui.output_data_frame("master_preview")),
        ui.nav_panel("Export", ui.output_text_verbatim("export_txt")),
        ui.nav_panel("Report", ui.output_text_verbatim("report_txt")),
    ),
    title="Industrial Data Augmentation Platform",
)


def server(input, output, session):
    project_manager = ProjectManager()
    registry = Registry()
    ingest_module = PackageIngestionModule()
    schema_module = SchemaValidationModule()
    profiling_module = ProfilingModule()
    harmonization_module = HarmonizationModule()
    augmentation_module = AugmentationRunModule()
    config_module = AugmentationConfigModule()
    merge_module = MergeBuildModule()
    report_module = ReportModule()

    input_msg = reactive.value("Bereit")
    aug_msg = reactive.value("Noch keine Augmentation durchgeführt")
    export_msg = reactive.value("Noch kein Export")
    last_quality = reactive.value(None)
    last_harmonized = reactive.value(pd.DataFrame())
    master_df = reactive.value(pd.DataFrame())

    def _ingest_one(path_str: str) -> None:
        package_dir = Path(path_str)
        record = ingest_module.ingest(package_dir)
        package_path = RAW_DIR / record["package_id"]
        tables = IngestionService.load_package_tables(package_path)

        issues: list[str] = []
        warnings: list[str] = []
        for filename, df in tables.items():
            result = schema_module.service.validate_table(filename, df)
            issues.extend(result.issues)
            warnings.extend(result.warnings)

        record["validation_status"] = "valid" if not issues else "invalid"
        record["augmentation_status"] = "not_started"
        record["included_in_master_dataset"] = False
        registry.upsert(record)

        if issues:
            input_msg.set(f"Importiert mit Fehlern: {issues}")
            return

        scenario_meta = json.loads((package_path / "scenario.json").read_text(encoding="utf-8"))
        quality = profiling_module.service.profile(
            tables["measurements_long.csv"],
            tables["events.csv"],
            tables["actuators.csv"],
        )
        harmonized = harmonization_module.service.build_harmonized(
            tables["measurements_long.csv"],
            tables["events.csv"],
            tables["actuators.csv"],
            scenario_meta,
            run_id=record["run_id"],
        )
        out_path = Path("storage/harmonized") / f"{record['package_id']}.parquet"
        harmonized.to_parquet(out_path, index=False)
        last_quality.set(quality)
        last_harmonized.set(harmonized.head(200))
        input_msg.set(f"Paket {record['package_id']} importiert. Warnungen: {warnings}")

    @reactive.effect
    @reactive.event(input.init_project)
    def _init_project():
        meta = project_manager.create_or_load(input.project_name(), input.owner())
        input_msg.set(f"Projekt geladen: {meta['project_name']} ({meta['version']})")

    @reactive.effect
    @reactive.event(input.ingest_btn)
    def _ingest_single():
        _ingest_one(input.package_dir())

    @reactive.effect
    @reactive.event(input.ingest_batch_btn)
    def _ingest_batch():
        for p in ["sample_data/package_001", "sample_data/package_002"]:
            _ingest_one(p)
        input_msg.set("Batch-Import abgeschlossen")

    @reactive.effect
    @reactive.event(input.augment_btn)
    def _augment_latest():
        reg = registry.load()
        valid = reg[reg["validation_status"] == "valid"] if not reg.empty else pd.DataFrame()
        if valid.empty:
            aug_msg.set("Keine validen Pakete für Augmentation")
            return
        latest = valid.iloc[-1]
        package_path = RAW_DIR / latest["package_id"]
        tables = IngestionService.load_package_tables(package_path)
        config = config_module.default()
        config.enabled = input.aug_methods()
        m, e, a = augmentation_module.run(
            tables["measurements_long.csv"],
            tables["events.csv"],
            tables["actuators.csv"],
            config,
        )
        scenario_meta = json.loads((package_path / "scenario.json").read_text(encoding="utf-8"))
        harmonized_aug = harmonization_module.service.build_harmonized(
            m,
            e,
            a,
            scenario_meta,
            run_id=latest["run_id"],
            is_augmented=True,
            augmentation_method=",".join(config.enabled),
        )
        out_path = Path("storage/harmonized") / f"{latest['package_id']}_aug.parquet"
        harmonized_aug.to_parquet(out_path, index=False)
        registry.update_status(latest["package_id"], augmentation_status="done")
        aug_msg.set(f"Augmentation fertig: {out_path.name}")

    @reactive.effect
    @reactive.event(input.build_btn)
    def _build_master():
        reg = registry.load()
        harmonized_files = sorted(Path("storage/harmonized").glob("*.parquet"))
        df = merge_module.service.build_master(harmonized_files)
        master_df.set(df.head(300))
        if not reg.empty:
            reg["included_in_master_dataset"] = True
            reg.to_csv("storage/processed/registry.csv", index=False)

    @reactive.effect
    @reactive.event(input.export_btn)
    def _export_master():
        if master_df().empty:
            export_msg.set("Master Dataset ist leer")
            return
        out = ExportModule.export_parquet(master_df(), FINAL_DIR / MASTER_DATASET_NAME)
        export_msg.set(f"Exportiert: {out}")

    @output
    @render.text
    def input_status():
        return input_msg()

    @output
    @render.data_frame
    def registry_table():
        return render.DataGrid(registry.load(), width="100%")

    @output
    @render.text
    def quality_txt():
        quality = last_quality()
        return json.dumps(quality, indent=2, default=str) if quality else "Noch keine Analyse"

    @output
    @render.plot
    def plot_signal():
        df = last_harmonized()
        if df.empty:
            return None
        sensor_cols = [c for c in df.columns if c.startswith("S")]
        if not sensor_cols:
            return None
        chart = df[["timestamp", sensor_cols[0]]].copy()
        chart["timestamp"] = pd.to_datetime(chart["timestamp"])
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(chart["timestamp"], chart[sensor_cols[0]])
        ax.set_title("Zeitreihe")
        return fig

    @output
    @render.plot
    def plot_events():
        df = last_harmonized()
        if df.empty or "event_type" not in df:
            return None
        counts = df["event_type"].fillna("none").value_counts()
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(6, 3))
        counts.plot(kind="bar", ax=ax)
        ax.set_title("Eventverteilung")
        return fig

    @output
    @render.data_frame
    def harmonized_table():
        return render.DataGrid(last_harmonized(), width="100%")

    @output
    @render.text
    def aug_txt():
        return aug_msg()

    @output
    @render.data_frame
    def master_preview():
        return render.DataGrid(master_df(), width="100%")

    @output
    @render.text
    def export_txt():
        return export_msg()

    @output
    @render.text
    def report_txt():
        reg = registry.load()
        return report_module.build_markdown(reg, last_quality()) + "\n\n" + LineageService.summarize(reg).to_string(index=False)


app = App(app_ui, server)
