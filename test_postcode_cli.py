"""Tests for the postcode CLI."""

# pylint: skip-file

import pytest


def test_cli_requires_mode_argument(run_shell_command):
    """Checks if running the CLI tool without a --mode/-m argument displays an error."""

    output, error = run_shell_command(f'python3 postcode_cli.py "FN1 3MR"')

    assert output == ""
    assert "the following arguments are required: --mode/-m" in error


def test_cli_requires_postcode_argument(run_shell_command):
    """Checks if running the CLI tool without a postcode argument displays an error."""

    output, error = run_shell_command(f'python3 postcode_cli.py --mode validate')

    assert output == ""
    assert "the following arguments are required: postcode" in error


def test_cli_requires_mode_and_postcode_arguments(run_shell_command):
    """Checks if running the CLI tool without both a --mode/-m argument and a postcode argument
    displays an error."""

    output, error = run_shell_command(f'python3 postcode_cli.py')

    assert output == ""
    assert "the following arguments are required: --mode/-m, postcode" in error


def test_cli_accepts_short_mode_argument(run_shell_command):
    """Checks if running the CLI tool with a --mode/-m argument does not display an error."""

    _, error = run_shell_command(f'python3 postcode_cli.py -m validate "FN1 3MR"')

    assert "" == error


@pytest.mark.parametrize("postcode", ["YYYYYY", "123456",
                                      "it is a truth universally acknowledged",
                                      "9", "Darkest Peru"])
def test_cli_outputs_correctly_on_invalid_postcodes(postcode, run_shell_command):

    output, _ = run_shell_command(f'python3 postcode_cli.py -m validate "{postcode}"')

    assert output.strip() == f'{postcode.upper().strip()} is not a valid postcode.'


@pytest.mark.parametrize("postcode", ["TN1 2FB", "SW2 3HJ", "YO11 1AA",
                                      "M2 1AB", "EH14 2AA"])
def test_cli_outputs_correctly_on_valid_postcodes(postcode, run_shell_command):

    output, _ = run_shell_command(f'python3 postcode_cli.py -m validate "{postcode}"')

    assert output.strip() == f'{postcode.upper().strip()} is a valid postcode.'


def test_cli_outputs_validated_postcode_in_correct_format(run_shell_command):

    output, _ = run_shell_command(f'python3 postcode_cli.py -m validate "  eH14 2aa  "')

    assert output.strip().startswith("EH14 2AA")


def test_cli_outputs_uncompletable_postcode_in_correct_format(run_shell_command):

    output, _ = run_shell_command(f'python3 postcode_cli.py -m complete "  eH14 2aaff  "')

    assert output.strip().endswith("EH14 2AAFF.")


@pytest.mark.parametrize("postcode", ["EH14 2AAFF", "palanquin", "123456",
                                      "000001", "The Emperor Nero"])
def test_cli_outputs_correctly_on_uncompletable_postcodes(postcode, run_shell_command):

    output, _ = run_shell_command(f'python3 postcode_cli.py -m complete "{postcode}"')

    assert output.strip() == f'No matches for {postcode.upper().strip()}.'


@pytest.mark.parametrize("postcode", ["S", "SW", "SW1", "SW1A"])
def test_cli_outputs_no_more_than_five_completions(postcode, run_shell_command):

    output, _ = run_shell_command(f'python3 postcode_cli.py -m complete "{postcode}"')

    assert len(output.strip().split("\n")) == 5


@pytest.mark.parametrize("postcode", ["SW1A 1BA"])
def test_cli_outputs_fewer_than_five_completions_when_relevant(postcode, run_shell_command):

    output, _ = run_shell_command(f'python3 postcode_cli.py -m complete "{postcode}"')

    assert len(output.strip().split("\n")) < 5


def test_cli_outputs_results_on_separate_lines(run_shell_command):

    output, _ = run_shell_command(f'python3 postcode_cli.py -m complete "T"')

    assert output.count("\n") == 5


@pytest.mark.parametrize("postcode", ("T", "F", "EH", "A", "SW1"))
def test_cli_outputs_valid_completions(postcode, run_shell_command):

    output, _ = run_shell_command(f'python3 postcode_cli.py -m complete "{postcode}"')

    for completion in output.splitlines():
        assert completion.startswith(postcode)
