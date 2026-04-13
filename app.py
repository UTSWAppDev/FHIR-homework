"""
FHIR Growth Chart Application - Scaffolded Starter
====================================================
Master of Science in Health Informatics
Application Development Exercise

This application demonstrates how to use the FHIR (Fast Healthcare
Interoperability Resources) standard to exchange healthcare data.

You will implement two key FHIR interactions:
  1. Fetching a list of patients from a FHIR server
  2. Fetching body weight observations to build a growth chart

FHIR Server Base URL: https://r4.smarthealthit.org
FHIR R4 Documentation: https://hl7.org/fhir/R4/
"""

from flask import Flask, render_template, abort
import requests

app = Flask(__name__)

# ---------------------------------------------------------------------------
# FHIR Server Configuration
# ---------------------------------------------------------------------------
FHIR_BASE_URL = "https://r4.smarthealthit.org"

# LOINC code for body weight (used when querying Observations)
BODY_WEIGHT_LOINC = "29463-7"

# HTTP headers required by FHIR servers
FHIR_HEADERS = {"Accept": "application/fhir+json"}


# ---------------------------------------------------------------------------
# Helper: extract a human-readable name from a FHIR Patient resource
# ---------------------------------------------------------------------------
def _extract_name(resource):
    """Return a display string from the first HumanName in a Patient resource."""
    names = resource.get("name", [])
    if not names:
        return "Unknown"
    name = names[0]
    given = " ".join(name.get("given", []))
    family = name.get("family", "")
    return f"{given} {family}".strip() or "Unknown"


# ---------------------------------------------------------------------------
# TODO 1 – Fetch the patient list from the FHIR server
# ---------------------------------------------------------------------------
def get_patients():
    """Fetch a list of patients from the FHIR server.

    Complete the steps below so that the function returns a list of patient
    dictionaries.  Each dictionary must contain these keys:

        {
            "id":        str,   # FHIR resource ID
            "name":      str,   # Human-readable full name
            "birthDate": str,   # e.g. "1990-05-15" or "Unknown"
            "gender":    str,   # e.g. "male" / "female" / "unknown"
        }

    Helpful references
    ------------------
    * FHIR Patient resource:   https://hl7.org/fhir/R4/patient.html
    * FHIR search parameters:  https://hl7.org/fhir/R4/search.html
    * Python requests library: https://docs.python-requests.org/

    Returns
    -------
    list[dict]
        A list of patient dictionaries (may be empty if the server returns
        no results).
    """

    # ------------------------------------------------------------------
    # TODO 1a – Build the endpoint URL for the Patient resource type.
    #
    # Pattern:  {FHIR_BASE_URL}/{ResourceType}
    # Example:  https://r4.smarthealthit.org/Patient
    # ------------------------------------------------------------------
    # url = f"{FHIR_BASE_URL}/Patient"

    # ------------------------------------------------------------------
    # TODO 1b – Define query parameters for the search request.
    #
    # Use "_count" to limit the number of results (e.g. 20 patients).
    # ------------------------------------------------------------------
    # params = {"_count": 20}

    # ------------------------------------------------------------------
    # TODO 1c – Make a GET request to the FHIR server.
    #
    # Pass the URL, FHIR_HEADERS, and params to requests.get().
    # Raise an exception if the response status code indicates an error.
    # ------------------------------------------------------------------
    # response = requests.get(url, headers=FHIR_HEADERS, params=params)
    # response.raise_for_status()

    # ------------------------------------------------------------------
    # TODO 1d – Parse the FHIR Bundle response.
    #
    # The response body is a FHIR Bundle.  Each entry in bundle["entry"]
    # has a "resource" key that contains the Patient resource.
    #
    # bundle = response.json()
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # TODO 1e – Extract patient data from the Bundle entries.
    #
    # Build a list of dictionaries using the schema shown in the docstring.
    # Use the _extract_name() helper to get a displayable full name.
    #
    # patients = []
    # for entry in bundle.get("entry", []):
    #     resource = entry.get("resource", {})
    #     patients.append(
    #         {
    #             "id":        resource.get("id"),
    #             "name":      _extract_name(resource),
    #             "birthDate": resource.get("birthDate", "Unknown"),
    #             "gender":    resource.get("gender", "Unknown"),
    #         }
    #     )
    # return patients
    # ------------------------------------------------------------------

    # Remove the line below once you have implemented the steps above.
    return []


# ---------------------------------------------------------------------------
# TODO 2 – Fetch body weight observations for a patient
# ---------------------------------------------------------------------------
def get_weight_observations(patient_id):
    """Fetch body weight Observations for a specific patient.

    Complete the steps below so that the function returns a list of
    observation dictionaries sorted by date.  Each dictionary must contain:

        {
            "date":  str,   # ISO date string, e.g. "2022-03-10"
            "value": float, # Numeric measurement (e.g. 72.5)
            "unit":  str,   # Unit of measure (e.g. "kg")
        }

    Helpful references
    ------------------
    * FHIR Observation resource: https://hl7.org/fhir/R4/observation.html
    * LOINC code for body weight: 29463-7
    * Observation search params: patient, code, _sort, _count

    Parameters
    ----------
    patient_id : str
        The FHIR resource ID of the patient whose weights you want.

    Returns
    -------
    list[dict]
        Observations sorted chronologically (oldest first).
    """

    # ------------------------------------------------------------------
    # TODO 2a – Build the endpoint URL for the Observation resource type.
    #
    # Pattern:  {FHIR_BASE_URL}/Observation
    # ------------------------------------------------------------------
    # url = f"{FHIR_BASE_URL}/Observation"

    # ------------------------------------------------------------------
    # TODO 2b – Define query parameters.
    #
    # Required parameters:
    #   "patient" – the patient_id passed into this function
    #   "code"    – the LOINC code for body weight (BODY_WEIGHT_LOINC)
    #
    # Optional but helpful:
    #   "_sort"  – sort by "date" so results come back chronologically
    #   "_count" – maximum number of results to return (e.g. 100)
    # ------------------------------------------------------------------
    # params = {
    #     "patient": patient_id,
    #     "code":    BODY_WEIGHT_LOINC,
    #     "_sort":   "date",
    #     "_count":  100,
    # }

    # ------------------------------------------------------------------
    # TODO 2c – Make a GET request to the FHIR server.
    # ------------------------------------------------------------------
    # response = requests.get(url, headers=FHIR_HEADERS, params=params)
    # response.raise_for_status()

    # ------------------------------------------------------------------
    # TODO 2d – Parse the FHIR Bundle response and extract observations.
    #
    # Each Observation resource contains:
    #   resource["effectiveDateTime"] – when the measurement was taken
    #   resource["valueQuantity"]["value"] – the numeric measurement
    #   resource["valueQuantity"]["unit"]  – the unit (e.g. "kg")
    #
    # bundle = response.json()
    # observations = []
    # for entry in bundle.get("entry", []):
    #     resource = entry.get("resource", {})
    #     value_quantity = resource.get("valueQuantity", {})
    #     observations.append(
    #         {
    #             "date":  resource.get("effectiveDateTime", "")[:10],
    #             "value": value_quantity.get("value"),
    #             "unit":  value_quantity.get("unit", "kg"),
    #         }
    #     )
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # TODO 2e – Sort observations chronologically and return them.
    #
    # return sorted(observations, key=lambda obs: obs["date"])
    # ------------------------------------------------------------------

    # Remove the line below once you have implemented the steps above.
    return []


# ---------------------------------------------------------------------------
# Flask Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Home page – displays a searchable list of patients."""
    patients = get_patients()
    return render_template("index.html", patients=patients)


@app.route("/patient/<patient_id>")
def patient_chart(patient_id):
    """Growth chart page – displays body weight over time for a patient."""
    observations = get_weight_observations(patient_id)

    if not observations:
        # Render the chart page with empty data so students can see the
        # "no data" state while they implement the FHIR call.
        return render_template(
            "patient.html",
            patient_id=patient_id,
            dates=[],
            weights=[],
            unit="kg",
        )

    dates = [obs["date"] for obs in observations]
    weights = [obs["value"] for obs in observations]
    unit = observations[0]["unit"]

    return render_template(
        "patient.html",
        patient_id=patient_id,
        dates=dates,
        weights=weights,
        unit=unit,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Set FLASK_DEBUG=1 in your environment to enable the debugger locally.
    import os
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode)
