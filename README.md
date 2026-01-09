# Postcodes

## Scenario

Your friend Mavis the Magnificent has asked you for your help. She's recently launched a local business which sends live magic tricks to your door; simply place an order on your phone, and a magician will be with you in less than thirty minutes to pull a rabbit out of a hat (or similar). Initially, you were worried she wanted your help with the actual tricks, but she has a different request: she wants you to use your programming skills to help her with logistical issues.

Currently, she spends a lot of time interacting with the [Postcodes API](https://postcodes.io/) to help her plan routes and schedules for her and the other magicians she employs. She'd like to have some simple scripts that she could run to get information out of the API, rather than having to manually craft URLs herself.

You don't have to start from scratch; before he was accidentally vanished, her glamorous assistant (Toby) had already laid some of the groundwork for the scripts.

## Setup and installation

Please ensure you do every step below carefully. Not doing so will mean we can't assess your work and **will result in a score of zero**.

1. Create a repo named exactly `Assessment-Networking-Week-1`
2. Invite your coaches to it (they'll let you know their Github usernames)
3. Push all the code in this folder to your created repository
4. On your created repo, click on `Actions` in the top menu bar
   - If it's there, click on `I understand my workflows, go ahead and enable them`
5. Create and activate a new virtual environment
6. Run `pip3 install -r requirements.txt` to install the required libraries
7. Complete the assessment
8. Commit & push your code regularly

## Quality assurance

Check the code quality with `pylint *.py`.

Run tests with `pytest -x`

## Tasks

There is a comprehensive test suite available for all tasks. Use the test suite to guide your code. You will be assessed on both passing tests (90%) and code quality (10%)

### Task 1

Complete the functions in [postcode_functions.py](./postcode_functions.py):

1. `validate_postcode()`
2. `get_postcode_for_location()`
3. `get_postcode_completions()`
4. `get_postcodes_details()`

Each function should interact with the [Postcodes API](https://postcodes.io/) making the minimum number of required calls. Functions should pass all associated tests in `test_postcode_functions.py`, handling all errors and returns appropriately.

### Task 2

Build a CLI tool in `postcode_cli.py` that functions as described below.

#### Arguments

When run, the script should accept the following arguments:

1. `--mode`/`-m` : a **required** argument that accepts only the values `validate` and `complete`
2. `postcode` : a **required** argument that accepts a string

- `python3 postcode_cli.py --mode validate "FN1 MR2"`
- `python3 postcode_cli.py -m validate "FN3 XF5"`
- `python3 postcode_cli.py --mode complete "FN1"`
- `python3 postcode_cli.py -m complete "FN3"`

#### Validation mode

When the script is run and the `--mode`/`-m` argument has the value of `validate`, the tool should check if the provided postcode is valid.

If the postcode is valid, the tool should output `'[postcode] is a valid postcode.'` only.

If the postcode is not valid, the tool should output `'[postcode] is not a valid postcode.'` only.

Regardless of how they are entered, postcodes should be checked/displayed as **uppercase-only** strings with no trailing spaces.

#### Completion mode

When the script is run and the `--mode`/`-m` argument has the value of `complete`, the tool should display valid postcodes that would complete the provided partial postcode.

Each valid completion should be displayed on its own line, as shown below. A maximum of **5** possible completions should be shown.

```
TN12 0AA
TN12 0AB
TN12 0AD
TN12 0AE
TN12 0AF
```

If there are no valid completions, the tool should display only `'No matches for [postcode].'`

### Task 3

Oops! Mavis has realised that all of these API calls are going to be a bit slow, and she wants to speed things up. She'd like you to add a caching mechanism to the scripts so that they don't have to make the same API calls over and over again.

The way Mavis wants her cache to work is to store the results of API calls in a file, and when the script is run again, it checks if the result is already in the cache before making a new API call. If it is, it uses the result that it already has instead of making a new API call.

Implement a caching mechanism to store the results of API calls and avoid redundant requests.

The cache should be stored in a file called `postcode_cache.json` in the same directory as the script. The cache should be a dictionary with the following structure:

```json
{
    "TN12 0AA": {
        "valid": true,
        "completions": ["TN12 0AA"]
    },
    "FN1": {
        "valid": false,
        "completions": ["FN1 MR2", "FN1 MR3", ...]
    }
}
```

The cache should be updated whenever a new API call is made, and the cache should be used to check if a postcode has already been validated or completed before making a new API call.
