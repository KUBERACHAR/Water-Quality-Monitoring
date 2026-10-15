# AI-Driven Water Quality Monitoring Dashboard

A Streamlit software prototype that simulates water-quality sensor readings, evaluates them with threshold rules and a weighted Water Quality Index (WQI), and displays the results in a live dashboard.

> **Prototype note:** This application generates random sample readings in software. It does not currently connect to physical sensors, an external API, or a user-provided file. Its "AI" analysis is a transparent formula and rule-based evaluation, not a trained machine-learning model.

## Features

- **Live Stream mode:** generates and evaluates a fresh simulated reading repeatedly.
- **Manual Input mode:** enter pH, turbidity, and TDS values and analyze them on demand.
- **Dashboard metrics:** pH, turbidity, total dissolved solids (TDS), WQI, status, and alerts.
- **Telemetry chart:** displays three illustrative points derived from the latest generated reading.

## How input is provided

Choose an input mode from the sidebar:

- **Manual Input:** enter pH (0–14), turbidity (0 or higher, in NTU), and TDS (0 or higher, in ppm) in the dashboard, then select **Analyze readings**. The submitted measurements are passed directly to `analyze_water_data()` and remain visible until another set is submitted. Values outside the analyzer's quality thresholds are accepted so that the dashboard can report them as warnings.
- **Live Stream (Auto-refresh):** the dashboard calls `simulate_sensor_input()` in `utils/simulation.py` to create a fresh virtual sensor payload on each update:

| Field | How it is generated |
| --- | --- |
| Device ID | Fixed value: `virtual_node_alpha` |
| Timestamp | Current local date and time in ISO format |
| pH | Random value from 6.0 to 9.0, rounded to 2 decimal places |
| Turbidity | Random value from 0.5 to 8.0 NTU, rounded to 2 decimal places |
| TDS | Random value from 150 to 550 ppm, rounded to 1 decimal place |

Each generated payload is passed to `analyze_water_data()` in `utils/ai_engine.py`. The device ID and timestamp are included in the simulated payload but are not currently shown in the dashboard.

There is no CSV upload or physical sensor/API integration in the current version.

## How analysis and outputs are generated

### Alerts

The analyzer checks each reading against these limits:

- **pH:** must be within the inclusive range 6.5–8.5.
- **Turbidity:** a warning is generated above 5.0 NTU.
- **TDS:** a warning is generated above 500 ppm.

Every exceeded limit adds a corresponding message to the active alerts section. These are the prototype's configured rules; they should not be treated as a substitute for local drinking-water standards or laboratory testing.

### Water Quality Index (WQI)

The dashboard computes three component scores, each floored at zero:

```text
pH score        = max(0, 100 - abs(7.2 - pH) × 30)
turbidity score = max(0, 100 - (turbidity / 10) × 100)
TDS score       = max(0, 100 - (TDS / 1000) × 100)
```

It combines them using a weighted average and rounds the result to one decimal place:

```text
WQI = round((pH score × 0.4) + (turbidity score × 0.3) + (TDS score × 0.3), 1)
```

The pH contribution has a 40% weight; turbidity and TDS each have a 30% weight. The score is displayed out of 100.

### Overall status

The status is selected from the WQI and alert results:

| Condition | Dashboard status |
| --- | --- |
| WQI is at least 80 **and** there are no threshold warnings | `OPTIMAL` |
| WQI is at least 50, but the `OPTIMAL` condition is not met | `WARNING` |
| WQI is below 50 | `HAZARDOUS` |

The status banner is green for `OPTIMAL`, yellow for `WARNING`, and red for `HAZARDOUS`. Any threshold messages are shown separately as active alerts.

### Telemetry chart

The line chart is illustrative, not stored measurement history. It plots three values derived from the current reading: pH at current minus 0.2, current minus 0.1, and current; turbidity at current minus 0.5, current minus 0.2, and current; and TDS at current minus 10, current minus 5, and current. In Manual Input mode, the chart is labeled to make clear that these are illustrative values, not historical readings.

## Run locally

Requirements: Python and the packages listed in `requirements.txt`.

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit in your browser. Use the sidebar to choose **Manual Input** or **Live Stream (Auto-refresh)**. In Manual Input mode, enter the three measurements and select **Analyze readings**. In live mode, the refresh interval can be set from 1 to 5 seconds (default: 2 seconds).

## Project structure

```text
app.py                 Streamlit interface, display, and refresh loop
utils/simulation.py    Random virtual sensor payload generation
utils/ai_engine.py     Threshold checks, WQI calculation, and status selection
requirements.txt       Python package requirements
```