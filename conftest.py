"""Fixtures used by multiple tests."""

# pylint: skip-file

import subprocess
import shlex
import pytest
import os
from postcode_functions import CACHE_FILE


@pytest.fixture
def bulk_postcodes():
    return {
        "status": 200,
        "result": [
            {
                "query": "SE5 2DE",
                "result": None
            },
            {
                "query": "YO31 2BS",
                "result": None
            },
            {
                "query": "NW1 2FE",
                "result": {
                    "postcode": "NW1 2FE",
                    "quality": 1,
                    "eastings": 529478,
                    "northings": 182467,
                    "country": "England",
                    "nhs_ha": "London",
                    "longitude": -0.13494,
                    "latitude": 51.526283,
                    "european_electoral_region": "London",
                    "primary_care_trust": "Camden",
                    "region": "London",
                    "lsoa": "Camden 023B",
                    "msoa": "Camden 023",
                    "incode": "2FE",
                    "outcode": "NW1",
                    "parliamentary_constituency": "Holborn and St Pancras",
                    "parliamentary_constituency_2024": "Holborn and St Pancras",
                    "admin_district": "Camden",
                    "parish": "Camden, unparished area",
                    "admin_county": None,
                    "date_of_introduction": "201411",
                    "admin_ward": "Regent's Park",
                    "ced": None,
                    "ccg": "NHS North Central London",
                    "nuts": "Camden",
                    "pfa": "Metropolitan Police",
                    "codes": {
                        "admin_district": "E09000007",
                        "admin_county": "E99999999",
                        "admin_ward": "E05013668",
                        "parish": "E43000197",
                        "parliamentary_constituency": "E14001290",
                        "parliamentary_constituency_2024": "E14001290",
                        "ccg": "E38000240",
                        "ccg_id": "93C",
                        "ced": "E99999999",
                        "nuts": "TLI36",
                        "lsoa": "E01000945",
                        "msoa": "E02000188",
                        "lau2": "E09000007",
                        "pfa": "E23000001"
                    }
                }
            }
        ]
    }


@pytest.fixture()
def run_shell_command():
    """Runs a command in the shell, returning any standard output and error messages."""

    def func(command):
        command = command.strip()

        if command.startswith("python3"):
            command = command.replace("python3", 'python3 -W "ignore"', 1)
        elif command.startswith("python"):
            command = command.replace("python", 'python -W "ignore"', 1)

        
        result = subprocess.run(shlex.split(command), capture_output=True)
        return result.stdout.decode("UTF-8"), result.stderr.decode("UTF-8")

    return func


@pytest.fixture(autouse=True)
def clear_cache_file():
    # Remove cache file before each test
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    yield
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)