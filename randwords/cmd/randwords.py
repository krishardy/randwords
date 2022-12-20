#!/usr/bin/env python3
import argparse
import random
import pathlib
import sys


def main():
    WORDS_DEFAULT=pathlib.Path(__file__).parent.parent / "words"
    BLOCKSIZE=2 ** 20  # 1MB

    parser = argparse.ArgumentParser(description="Random word generator")
    parser.add_argument("-f", "--file", type=str, help="Dictionary file. (Default: %(default)s)", default=WORDS_DEFAULT)
    parser.add_argument("count", type=int, help="Number of words to generate")
    parser.add_argument("-a", "--no-apostrophe", action="store_true", help="Do not include apostrophes")
    parser.add_argument("-l", "--lower", action="store_true", help="make all strings lowercase")
    parser.add_argument("-A", "--ascii-only", action="store_true", help="Include only ASCII characters")
    parser.add_argument("-s", "--sort", action="store_true", help="Alphabetically sort the words")
    args = parser.parse_args()

    newline_count = 0

    with open(args.file, "r") as fh:

        # Count number of lines by reading one block at a time
        while (True):
            try:
                buffer = fh.read(BLOCKSIZE)
                if len(buffer) == 0:
                    break
            except Exception:
                break
            newline_count += buffer.count('\n')

        # Now start at the beginning of the file and start randomly picking lines
        fh.seek(0)

        words = []
        while len(words) < args.count:
            choices = []
            for i in range(args.count):
                choices.append(random.randint(0, newline_count))
            choices = sorted(choices)  # Order for faster lookups

            word_idx = 0
            choices_idx = 0
            prepend = ""
            while (len(words) < args.count):
                try:
                    buffer_start = 0
                    buffer = prepend + fh.read(BLOCKSIZE)
                    prepend = ""
                    if len(buffer) == 0:
                        break
                except Exception:
                    break

                while buffer_start < len(buffer):
                    newline_pos = buffer.find('\n', buffer_start)
                    if newline_pos == -1:
                        prepend = buffer[buffer_start:]
                        break
                    if word_idx == choices[choices_idx]:
                        word = buffer[buffer_start:newline_pos]
                        if args.no_apostrophe:
                            word = word.replace("'", "")
                        if args.ascii_only:
                            word = word.encode("ascii", "ignore")
                            word = word.decode()
                        if args.lower:
                            word = word.lower()
                        words.append(word)
                        choices_idx += 1
                        if choices_idx >= len(choices):
                            break
                    buffer_start = newline_pos + 1
                    word_idx += 1

    # Randomize the word order if necessary
    if args.sort == False:
        random.shuffle(words)

    print(' '.join(words))
    return 0

if __name__ == "__main__":
    sys.exit(main())