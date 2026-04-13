# FHIR Growth Chart — Pre-Work Exercise

**Master of Science in Health Informatics | Application Development**
UT Southwestern Medical Center

---

## Overview

In this exercise you will complete a scaffolded Flask web application that
uses the **FHIR R4** (Fast Healthcare Interoperability Resources) standard
to exchange healthcare data with a public sandbox server.

By the end you will have a working application that:

1. Displays a searchable list of patients retrieved from a FHIR server.
2. Renders an interactive **body weight growth chart** for any selected patient.

The heavy lifting of the web framework is already done for you.  Your job is
to fill in the two FHIR API calls marked with **TODO** comments inside
`app.py`.

---

## Learning Objectives

- Understand the structure of a **FHIR RESTful API**.
- Query a FHIR server for **Patient** and **Observation** resources.
- Parse **FHIR Bundle** responses in Python.
- Integrate external API data into a Flask web application.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.10 or newer |
| pip | included with Python |
| Internet access | required (public FHIR sandbox) |

---

## Project Structure

```
FHIR-homework/
├── app.py              ← Flask application (you will edit this)
├── requirements.txt    ← Python dependencies
└── templates/
    ├── base.html       ← Shared HTML layout
    ├── index.html      ← Patient list page
    └── patient.html    ← Growth chart page
```

---

## Setup Instructions

### Step 1 — Clone the repository

```bash
git clone <repository-url>
cd FHIR-homework
```

### Step 2 — Create and activate a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the application

```bash
python app.py
```

Open your browser and navigate to **http://127.0.0.1:5000**.

You should see the patient list page with a warning that no patients have
been loaded yet.  You will fix that in the next section.

---

## FHIR Background

### What is FHIR?

FHIR (Fast Healthcare Interoperability Resources) is the modern standard for
exchanging healthcare data electronically.  It is published by HL7 and is
built on familiar web technologies: **REST**, **JSON**, and **HTTP**.

### FHIR Resources

Everything in FHIR is a **Resource** — a structured data object that
represents a clinical or administrative concept.

| Resource | Represents |
|----------|-----------|
| `Patient` | A person receiving healthcare |
| `Observation` | A measurement or assertion (e.g. body weight) |
| `Condition` | A clinical diagnosis |
| `MedicationRequest` | A prescription |

### FHIR REST API Pattern

```
GET {base-url}/{ResourceType}
GET {base-url}/{ResourceType}/{id}
GET {base-url}/{ResourceType}?{search-parameter}={value}
```

The **FHIR server** for this exercise is:

```
https://r4.smarthealthit.org
```

### FHIR Bundles

When you search for resources, the server returns a **Bundle** — a JSON
object that wraps one or more resources:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 20,
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "87a339d0-8cae-11e8-9eb6-529269fb1459",
        "name": [{ "family": "Smith", "given": ["John"] }],
        "birthDate": "1990-05-15",
        "gender": "male"
      }
    }
  ]
}
```

---

## Your Tasks

Open `app.py` in your editor.  You will implement two functions.

---

### TODO 1 — `get_patients()`

**Goal:** Return a list of patients from the FHIR server.

#### Step 1a — Build the Patient endpoint URL

The FHIR Patient resource endpoint follows this pattern:

```
{FHIR_BASE_URL}/{ResourceType}
```

In Python:

```python
url = f"{FHIR_BASE_URL}/Patient"
```

#### Step 1b — Define query parameters

Use `_count` to limit the number of returned patients:

```python
params = {"_count": 20}
```

> **FHIR Tip:** The `_count` parameter is a standard FHIR search parameter
> supported by all compliant servers.

#### Step 1c — Make the HTTP GET request

Use the `requests` library.  Always pass `FHIR_HEADERS` so the server knows
you expect a FHIR JSON response:

```python
response = requests.get(url, headers=FHIR_HEADERS, params=params)
response.raise_for_status()   # raises an exception on HTTP 4xx/5xx errors
```

#### Step 1d — Parse the JSON response

```python
bundle = response.json()
```

The variable `bundle` is now a Python dictionary that mirrors the JSON
structure shown in the *FHIR Bundles* section above.

#### Step 1e — Extract patient data from the Bundle entries

Each entry in `bundle["entry"]` has a `"resource"` key containing the
Patient resource.  Extract the fields you need:

```python
patients = []
for entry in bundle.get("entry", []):
    resource = entry.get("resource", {})
    patients.append(
        {
            "id":        resource.get("id"),
            "name":      _extract_name(resource),   # helper already provided
            "birthDate": resource.get("birthDate", "Unknown"),
            "gender":    resource.get("gender", "Unknown"),
        }
    )
return patients
```

> **Checkpoint:** After removing the `return []` stub and saving, restart
> Flask and refresh the browser.  You should see a table of patients.

---

### TODO 2 — `get_weight_observations(patient_id)`

**Goal:** Return body weight observations for a given patient, sorted by date.

#### Step 2a — Build the Observation endpoint URL

```python
url = f"{FHIR_BASE_URL}/Observation"
```

#### Step 2b — Define query parameters

Body weight is identified by **LOINC code 29463-7**.  Search for
Observations belonging to the selected patient with that code:

```python
params = {
    "patient": patient_id,
    "code":    BODY_WEIGHT_LOINC,   # constant already defined at the top of app.py
    "_sort":   "date",
    "_count":  100,
}
```

> **FHIR Tip:** The `code` search parameter accepts LOINC codes in the
> format `{system}|{code}` (e.g. `http://loinc.org|29463-7`), but many
> servers also accept the bare code `29463-7`.

#### Step 2c — Make the HTTP GET request

```python
response = requests.get(url, headers=FHIR_HEADERS, params=params)
response.raise_for_status()
```

#### Step 2d — Parse the Bundle and extract observation data

Each Observation resource stores the numeric value inside `valueQuantity`:

```json
{
  "resourceType": "Observation",
  "effectiveDateTime": "2022-03-10T08:30:00+00:00",
  "valueQuantity": {
    "value": 72.5,
    "unit": "kg",
    "system": "http://unitsofmeasure.org",
    "code": "kg"
  }
}
```

Extract the fields you need:

```python
bundle = response.json()
observations = []
for entry in bundle.get("entry", []):
    resource = entry.get("resource", {})
    value_quantity = resource.get("valueQuantity", {})
    observations.append(
        {
            "date":  resource.get("effectiveDateTime", "")[:10],  # YYYY-MM-DD
            "value": value_quantity.get("value"),
            "unit":  value_quantity.get("unit", "kg"),
        }
    )
```

#### Step 2e — Sort observations chronologically and return

```python
return sorted(observations, key=lambda obs: obs["date"])
```

> **Checkpoint:** After removing the `return []` stub and saving, restart
> Flask and click *View Chart* next to any patient.  If the patient has
> weight observations, you will see the interactive line chart and the raw
> data table below it.

---

## Testing Your Implementation

### Manual Testing Checklist

- [ ] The home page (`/`) displays a list of patients.
- [ ] The search box filters patients by name in real time.
- [ ] Clicking *View Chart* navigates to `/patient/<id>`.
- [ ] Patients with weight data display a line chart.
- [ ] The summary cards show the correct number of observations, min, and max weight.
- [ ] The raw data table shows the correct dates and values.

### Exploring the FHIR API Directly

You can explore the FHIR server from your browser or a tool like
[Hoppscotch](https://hoppscotch.io):

**List patients:**
```
GET https://r4.smarthealthit.org/Patient?_count=5
```

**Get weight observations for a patient:**
```
GET https://r4.smarthealthit.org/Observation?patient=<id>&code=29463-7
```

Replace `<id>` with a patient ID you see in the application.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "No patients loaded" warning | `get_patients()` still returns `[]` | Complete TODO 1 |
| "No weight observations found" | `get_weight_observations()` still returns `[]` | Complete TODO 2 |
| `ConnectionError` | No internet access | Check your network connection |
| `requests.exceptions.HTTPError` | Bad URL or parameters | Print `response.text` to see the FHIR error message |
| Chart does not render | Patient has no weight observations in the sandbox | Try a different patient |

---

## Reference Links

| Resource | URL |
|----------|-----|
| FHIR R4 Specification | https://hl7.org/fhir/R4/ |
| FHIR Patient Resource | https://hl7.org/fhir/R4/patient.html |
| FHIR Observation Resource | https://hl7.org/fhir/R4/observation.html |
| FHIR Search Parameters | https://hl7.org/fhir/R4/search.html |
| SMART Health IT Sandbox | https://r4.smarthealthit.org |
| LOINC Code 29463-7 | https://loinc.org/29463-7/ |
| Python requests library | https://docs.python-requests.org/ |
| Flask documentation | https://flask.palletsprojects.com/ |

---

## Submission

Once your application is working, push your completed `app.py` to your
forked repository and submit the link via the course portal.

---

*UT Southwestern Medical Center — Master of Science in Health Informatics*
