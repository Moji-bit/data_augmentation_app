# Industrial Data Augmentation Platform (Shiny for Python Core)

Produktionsorientierte, modulare Plattform für inkrementelle Verarbeitung industrieller Zeitreihen- und Eventdaten.

## Features

- Projektbasiertes Arbeiten mit Versionierung
- Ingestion von Szenario-Paketen (4-Dateien-Standard)
- Registry mit Paketstatus, Validierung, Augmentation, Master-Inclusion
- Schema-Validierung und Schema-Drift-Warnungen
- Harmonisierung (Long→Wide, Join über `timestamp + scenario_id`)
- Data Quality Scoring (hoch/mittel/niedrig + ML-Readiness)
- Augmentation für Zeitreihen, Events, Aktorik
- Inkrementeller Workflow (append-only + dedup)
- Build und Export von **einem** Master-Dataset:
  - `storage/final/dataset_master.parquet`
- Data Lineage Reporting

## Projektstruktur

Siehe Ordnerstruktur in der Aufgabenstellung; alle geforderten Module/Services/Models wurden angelegt.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## App starten

```bash
shiny run --reload app.py
```

## Workflow

1. Projekt in der Sidebar anlegen/laden.
2. Einzelpaket importieren (`sample_data/package_001`) oder Batch-Import starten.
3. Validierungs-/Quality-Status in den Tabs prüfen.
4. Augmentation ausführen (nur nach Analyse, durch UI-Reihenfolge unterstützt).
5. Master-Dataset bauen und exportieren.

## Testen

```bash
pytest -q
```

## Beispiel-Daten

- `sample_data/package_001/*`
- `sample_data/package_002/*`

## Beispiel Master-Dataset

- `storage/final/dataset_master.parquet` (wird bereitgestellt und kann neu erzeugt werden)

## Architekturhinweis

- **Shiny Core API**: `app.py` enthält ausschließlich UI + Server Wiring.
- **Business-Logik** liegt in `services/`.
- **Feature-Module** bündeln Workflows in `modules/`.
- **Modelle/Konfigs** sind in `models/` definiert.

