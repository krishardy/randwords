#!/usr/bin/env python3
import argparse
import secrets
import string
import sys

def main():
    parser = argparse.ArgumentParser(description="Random string generator")
    parser.add_argument("count", type=int, help="Number of characters to generate")
    parser.add_argument("-u", "--no-uppercase", action="store_true",
        help="Do not include upper case characters")
    parser.add_argument("-l", "--no-lowercase", action="store_true",
        help="Do not include lower case characters")
    parser.add_argument("-0", "--no-numbers", action="store_true",
        help="Do not include numbers")
    parser.add_argument("-s", "--special", type=str, default="",
        help="Special characters to include")
    args = parser.parse_args()

    source_string = set(list(args.special))
    if args.no_uppercase == False:
        source_string = source_string.union(list(string.ascii_uppercase))
    if args.no_lowercase == False:
        source_string = source_string.union(list(string.ascii_lowercase))
    if args.no_numbers == False:
        source_string = source_string.union(list(string.digits))

    if len(source_string) == 0:
        print("There are no available characters in the character set. Aborting.")
        exit(1)

    source_string = ''.join(source_string)

    print(''.join(secrets.choice(source_string) for i in range(args.count)))
    return 0

if __name__ == "__main__":
    sys.exit(main())