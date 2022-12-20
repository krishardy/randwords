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
                buf = fh.read(BLOCKSIZE)
                if len(buf) == 0:
                    break
            except Exception:
                break
            newline_count += buf.count('\n')

        # Now start at the beginning of the file and start randomly picking lines
        fh.seek(0)

        choices = []
        for _ in range(args.count):
            choices.append(random.randint(0, newline_count))
        choices = sorted(choices)  # Order so that we don't have to seek

        choices_idx = 0
        words = []
        line_num = 0
        prepend = ""
        while (len(words) < args.count):
            # Read a block
            try:
                buf = prepend + fh.read(BLOCKSIZE)
                prepend = ""
                if len(buf) == 0:
                    break  # We've hit the end of the file
            except Exception as e:
                print(e)
                break

            prev_buf_start = -1
            buf_start = 0
            while (buf_start < len(buf)) and (choices_idx < len(choices)):
                # Search for the correct line, one line at a time
                if buf_start != prev_buf_start:
                    prev_buf_start = buf_start
                    newline_pos = buf.find('\n', buf_start)
                    if newline_pos == -1:
                        # Newline not found. Cache the remaining buffer to prepend it to the buffer on the next read
                        prepend = buf[buf_start:]
                        break

                if line_num == choices[choices_idx]:
                    # The line is one in our selection. Grab it, clean it as necessary and save it.
                    word = buf[buf_start:newline_pos]
                    if args.no_apostrophe:
                        word = word.replace("'", "")
                    if args.ascii_only:
                        word = word.encode("ascii", "ignore")
                        word = word.decode()
                    if args.lower:
                        word = word.lower()
                    words.append(word)
                    choices_idx += 1
                else:
                    buf_start = newline_pos + 1
                    line_num += 1
    
    if len(words) < args.count:
        print(f"An error occurred and only {len(words)} words were selected")

    # Randomize the word order if necessary
    if args.sort == False:
        random.shuffle(words)
    else:
        words = sorted(words)

    print(' '.join(words))
    return 0

if __name__ == "__main__":
    sys.exit(main())
