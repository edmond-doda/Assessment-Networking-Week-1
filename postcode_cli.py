"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        '--mode', '-m', required=True, help="Select which mode you would like: 'validate' or 'complete'")

    parser.add_argument('postcode', type=str,
                        help="Enter a valid UK postcode as a string")

    args = parser.parse_args()

    if args.mode not in ['validate', 'complete']:
        parser.error('Mode must be either validate or complete')

    formatted_postcode = args.postcode.upper().strip()

    if args.mode == 'validate':
        if validate_postcode(args.postcode):
            print(f'{formatted_postcode} is a valid postcode.')
        else:
            print(f'{formatted_postcode} is not a valid postcode.')

    if args.mode == 'complete':
        completed_postcodes = get_postcode_completions(args.postcode)
        if not completed_postcodes:
            print(f'No matches for {formatted_postcode}.')
        for postcode in completed_postcodes:
            print(postcode)
