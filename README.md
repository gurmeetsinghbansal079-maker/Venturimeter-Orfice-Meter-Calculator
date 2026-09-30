# FlowLab — Venturimeter & Orifice Meter Calculator

Python mini project for **Problem No. 14** in Diploma Mechanical Engineering, Semester 3.

FlowLab converts a differential-manometer reading into pressure difference, theoretical discharge, actual discharge, and pipe velocities. It also compares a Venturimeter with an orifice meter for the same pipe geometry.

## Main features

- Venturimeter and orifice-meter modes
- Water, kerosene, light oil, glycerin, or custom flowing-liquid density
- Mercury, carbon tetrachloride, salt solution, or custom manometer-liquid density
- Input validation for impossible geometry and density combinations
- Pressure difference and differential-head calculation
- Theoretical and actual discharge in m³/s, L/s, and L/min
- Inlet and throat/orifice velocity
- Animated meter and U-tube manometer schematic
- Discharge-versus-deflection comparison graph
- Formula substitution, textbook verification case, theory, and viva questions
- CSV result download
- Mobile-responsive layout for Android

## Engineering equations

For a horizontal pipe with a heavier differential-manometer liquid:

```text
Δp = (ρm − ρf) g x
h  = Δp / (ρf g)

A1 = πD1²/4
A2 = πD2²/4

Qth = (A1 A2 / √(A1² − A2²)) √(2gh)
Qa  = Cd × Qth
```

The model assumes steady, incompressible flow and negligible elevation difference between pressure taps.

## Run on a computer

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install the libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL shown in the terminal, normally `http://localhost:8501`.

## Run the tests

```bash
pip install pytest
pytest -q
```

## Upload to GitHub

Upload the complete contents of this folder, keeping the `.streamlit` and `tests` folders. The repository must contain `app.py` and `requirements.txt` at its top level.

Suggested repository name:

```text
venturi-orifice-flowlab
```

Suggested description:

```text
Venturimeter and orifice meter discharge calculator built with Python and Streamlit.
```

## Deploy on Streamlit Community Cloud

1. Open [Streamlit Community Cloud](https://share.streamlit.io/).
2. Choose **Create app** → **Deploy a public app from GitHub**.
3. Select your GitHub repository and the `main` branch.
4. Enter `app.py` as the main file path.
5. Click **Deploy**.

## Project files

```text
app.py                         Streamlit user interface
meter_calculations.py          Tested engineering calculation functions
requirements.txt               Deployment libraries
MANUAL_TEST_CASE.md            Manual-versus-app verification for the report
.streamlit/config.toml         App theme and server settings
tests/test_meter_calculations.py
tests/test_streamlit_app.py
```

## Project members

- **25012250610070 — KAVYA KOTHARI**
- **25012251210009 — PATEL JAINIL RAJESH**
- **25012250610055 — PATIL RISHABH VALMIK**

To update the assigned group, edit `PROJECT_MEMBERS` near the top of `app.py` before submission.
