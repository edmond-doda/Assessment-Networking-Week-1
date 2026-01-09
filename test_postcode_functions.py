"""Tests for the postcode functions."""

# pylint: skip-file

import pytest
import requests as req

from postcode_functions import (get_postcode_completions, get_postcode_for_location,
                                get_postcodes_details, validate_postcode)


## Validate tests


@pytest.mark.parametrize("postcode", [42, True, 4.2, None,
                                      ("postcode1", "postcode2"),
                                      ["postcode1", "postcode2"]])
def test_validate_postcode_rejects_non_string_inputs(postcode):
    with pytest.raises(TypeError, match="Function expects a string."):
        validate_postcode(postcode)


@pytest.mark.parametrize("postcode", ["VALID1", "VALID2", "VALID3"])
def test_validate_postcode_returns_true_valid_postcode(postcode, requests_mock):
    requests_mock.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate",
        status_code=200, json={"result": True})
    assert validate_postcode(postcode)


def test_validate_postcode_returns_boolean(requests_mock):
        requests_mock.get(
        f"https://api.postcodes.io/postcodes/TEST/validate",
        status_code=200, json={"result": True})

        assert isinstance(validate_postcode("TEST"), bool)

        requests_mock.get(
        f"https://api.postcodes.io/postcodes/TEST/validate",
        status_code=200, json={"result": False})

        assert isinstance(validate_postcode("TEST"), bool)


@pytest.mark.parametrize("postcode", ["INVALID1", "INVALID2", "INVALID3"])
def test_validate_postcode_returns_false_invalid_postcode(postcode, requests_mock):
    requests_mock.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate",
        status_code=200, json={"result": False})
    assert not validate_postcode(postcode)


def test_validate_postcode_raises_exception_with_500_codes(requests_mock):
    requests_mock.get(
        f"https://api.postcodes.io/postcodes/ABC/validate", status_code=500)
    with pytest.raises(req.RequestException, match="Unable to access API."):
        validate_postcode("ABC")


def test_validate_postcode_calls_get_once(requests_mock):
    requests_mock.get(
        f"https://api.postcodes.io/postcodes/ABC/validate",
        status_code=200, json={"result": True})
    validate_postcode("ABC")
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].method == 'GET'


# Locations tests


@pytest.mark.parametrize("lat, long",
                         [(True, False), (3.5, "not float"),
                          (None, 3.5), ("not float", "also not float")])
def test_get_postcode_for_location_rejects_non_floats(lat, long):
    with pytest.raises(TypeError, match="Function expects two floats."):
        get_postcode_for_location(lat, long)


def test_get_postcode_for_location_raises_exception_with_500_codes(requests_mock):
    requests_mock.get(
        "https://api.postcodes.io/postcodes?lon=1.0&lat=2.0", status_code=500)
    with pytest.raises(req.RequestException, match="Unable to access API."):
        get_postcode_for_location(2.0, 1.0)


def test_get_postcode_for_locations_calls_get_once(requests_mock):
    requests_mock.get(
        "https://api.postcodes.io/postcodes?lon=1.0&lat=2.0",
        status_code=200, json={"result": [{"postcode": "F"}]})
    get_postcode_for_location(2.0, 1.0)
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].method == 'GET'


def test_get_postcode_for_location_raises_error_no_result(requests_mock):
    requests_mock.get(
        "https://api.postcodes.io/postcodes?lon=1.0&lat=2.0",
        status_code=200, json={"result": None})
    with pytest.raises(ValueError, match="No relevant postcode found."):
        get_postcode_for_location(2.0, 1.0)


def test_get_postcode_for_location_returns_result(requests_mock):
    requests_mock.get(
        "https://api.postcodes.io/postcodes?lon=1.0&lat=2.0",
        status_code=200, json={"result": [
                {"postcode": "P0STC0DE"},
                {"postcode": "further away"}
            ]})
    assert get_postcode_for_location(2.0, 1.0) == "P0STC0DE"


# Completions tests


@pytest.mark.parametrize("postcode_start", [True, False, None, 42, ("str", "str")])
def test_get_postcode_completions_rejects_non_string(postcode_start):
    with pytest.raises(TypeError, match="Function expects a string."):
        get_postcode_completions(postcode_start)

def test_get_postcode_completions_calls_get_once(requests_mock):
    requests_mock.get(
        "https://api.postcodes.io/postcodes/abc/autocomplete", status_code=200, json={"result": []})
    get_postcode_completions("abc")
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].method == 'GET'


def test_get_postcode_completions_raises_error_with_500_codes(requests_mock):
    requests_mock.get(
        "https://api.postcodes.io/postcodes/abc/autocomplete", status_code=500, json={"result": []})
    with pytest.raises(req.RequestException, match="Unable to access API."):
        get_postcode_completions("abc")


def test_get_postcode_completions_returns_result_value(requests_mock):
    requests_mock.get("https://api.postcodes.io/postcodes/abc/autocomplete",
                      status_code=200, json={"result": ["abcdef"]})
    assert get_postcode_completions("abc") == ["abcdef"]


# Postcodes details tests


@pytest.mark.parametrize("postcodes", ["not a list", 42, 64.5, None, True, False])
def test_get_postcodes_details_rejects_non_list(postcodes):
    with pytest.raises(TypeError, match="Function expects a list of strings."):
        get_postcodes_details(postcodes)


@pytest.mark.parametrize("postcodes", [
    ["string", 42], ["string", "also string", 42],
    [True, False, "string"], ["postcode1", "postcode2", None], ["", None]
])
def test_get_postcodes_details_rejects_non_list_of_strings(postcodes):
    with pytest.raises(TypeError, match="Function expects a list of strings."):
        get_postcodes_details(postcodes)


def test_get_postcodes_details_calls_post_once(requests_mock):
    requests_mock.post("https://api.postcodes.io/postcodes",
                       json={
                            "status": 200,
                            "result": [
                                {
                                    "query": "postcode1",
                                    "result": None
                                },
                                {
                                    "query": "postcode2",
                                    "result": None
                                }
                            ]
                        })
    get_postcodes_details(["postcode1", "postcode2"])
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].method == 'POST'


def test_get_postcodes_details_raises_exception_with_500_codes(requests_mock):
    requests_mock.post("https://api.postcodes.io/postcodes", status_code=500)
    with pytest.raises(req.RequestException, match="Unable to access API."):
        get_postcodes_details([])


def test_get_postcodes_details_returns_expected_data(requests_mock, bulk_postcodes):
    requests_mock.post("https://api.postcodes.io/postcodes",
                       status_code=200, json=bulk_postcodes)
    result = get_postcodes_details(["SE5 2DE", "YO31 2BS", "NW1 2FE"])

    assert result[0]["result"] == None
    assert result[2]["result"]["primary_care_trust"] == "Camden"
    assert result[2]["result"]["primary_care_trust"] == "Camden"
    assert result[2]["result"]["codes"]["parish"] == "E43000197"


def test_get_postcodes_details_returns_response_list(requests_mock):
    requests_mock.post("https://api.postcodes.io/postcodes",
                       status_code=200, json={
                                            "status": 200,
                                            "result": []
                                        })
    response = get_postcodes_details([])
    assert isinstance(response, list)
    assert len(response) == 0


