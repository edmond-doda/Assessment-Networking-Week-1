"""Tests for postcode caching functionality."""

import os
import json
import pytest
from postcode_functions import (
    validate_postcode, get_postcode_completions, get_postcodes_details, load_cache, save_cache, CACHE_FILE
)


def test_validate_postcode_caches_result(requests_mock):
    requests_mock.get(
        "https://api.postcodes.io/postcodes/ABC123/validate",
        status_code=200, json={"result": True})
    # First call should hit API
    assert validate_postcode("ABC123") is True
    # Second call should use cache, not API
    requests_mock.reset_mock()
    assert validate_postcode("ABC123") is True
    assert requests_mock.call_count == 0
    # Check cache file content
    cache = load_cache()
    assert "ABC123" in cache
    assert cache["ABC123"]["valid"] is True


@pytest.mark.parametrize("postcode,api_result", [
    ("ABC123", True),
    ("ZZ99 9ZZ", False),
    ("EC1A 1BB", True),
])
def test_validate_postcode_caches_result_param(postcode, api_result, requests_mock):
    requests_mock.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate",
        status_code=200, json={"result": api_result}
    )
    # First call should hit API
    assert validate_postcode(postcode) is api_result
    # Second call should use cache, not API
    requests_mock.reset_mock()
    assert validate_postcode(postcode) is api_result
    assert requests_mock.call_count == 0
    # Check cache file content
    cache = load_cache()
    assert postcode in cache
    assert cache[postcode]["valid"] is api_result


def test_get_postcode_completions_caches_result(requests_mock):
    requests_mock.get(
        "https://api.postcodes.io/postcodes/AB/autocomplete",
        status_code=200, json={"result": ["AB1 1AA", "AB1 2BB"]})
    # First call should hit API
    assert get_postcode_completions("AB") == ["AB1 1AA", "AB1 2BB"]
    # Second call should use cache, not API
    requests_mock.reset_mock()
    assert get_postcode_completions("AB") == ["AB1 1AA", "AB1 2BB"]
    assert requests_mock.call_count == 0
    # Check cache file content
    cache = load_cache()
    assert "AB" in cache
    assert cache["AB"]["completions"] == ["AB1 1AA", "AB1 2BB"]


@pytest.mark.parametrize("postcode_start,completions", [
    ("AB", ["AB1 1AA", "AB1 2BB"]),
    ("XY", ["XY9 9XY"]),
    ("QW", []),
])
def test_get_postcode_completions_caches_result_param(postcode_start, completions, requests_mock):
    requests_mock.get(
        f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete",
        status_code=200, json={"result": completions}
    )
    # First call should hit API
    assert get_postcode_completions(postcode_start) == completions
    # Second call should use cache, not API
    requests_mock.reset_mock()
    assert get_postcode_completions(postcode_start) == completions
    assert requests_mock.call_count == 0
    # Check cache file content
    cache = load_cache()
    assert postcode_start in cache
    assert cache[postcode_start]["completions"] == completions


def test_cache_preserves_both_valid_and_completions(requests_mock):
    # Validate postcode
    requests_mock.get(
        "https://api.postcodes.io/postcodes/ZZ1 1ZZ/validate",
        status_code=200, json={"result": True})
    validate_postcode("ZZ1 1ZZ")
    # Add completions for same postcode start
    requests_mock.get(
        "https://api.postcodes.io/postcodes/ZZ/autocomplete",
        status_code=200, json={"result": ["ZZ1 1ZZ", "ZZ2 2ZZ"]})
    get_postcode_completions("ZZ")
    cache = load_cache()
    assert "ZZ1 1ZZ" in cache and "valid" in cache["ZZ1 1ZZ"]
    assert "ZZ" in cache and "completions" in cache["ZZ"]


def test_save_and_load_cache_roundtrip():
    data = {"A": {"valid": True}, "B": {"completions": ["B1"]}}
    save_cache(data)
    loaded = load_cache()
    assert loaded == data


@pytest.mark.parametrize("data", [
    {"A": {"valid": True}},
    {"B": {"completions": ["B1"]}},
    {"A": {"valid": False}, "B": {"completions": ["B1", "B2"]}},
])
def test_save_and_load_cache_roundtrip_param(data):
    save_cache(data)
    loaded = load_cache()
    assert loaded == data
