import io
import os
import sys
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Uppercase runes
uppercase_runes = {
    "A": "ᚪ",
    "B": "ᛔ",
    "C": "ᛈ",
    "D": "ᚣ",
    "E": "ᚯ",
    "F": "ᚡ",
    "G": "ᛥ",
    "H": "ᚻ",
    "I": "ᛂ",
    "J": "ᚵ",
    "K": "ᛯ",
    "L": "ᛚ",
    "M": "ᛗ",
    "N": "ᚬ",
    "O": "ᛟ",
    "P": "ᚹ",
    "Q": "ᚿ",
    "R": "ᚱ",
    "S": "ᛊ",
    "T": "ᛏ",
    "U": "ᚤ",
    "V": "ᛤ",
    "W": "ᛠ",
    "X": "ᚷ",
    "Y": "ᛉ",
    "Z": "ᛢ",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "0": "0",
    "(": "(",
    ")": ")",
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "=": "=",
    ",": ",",
    ".": ".",
    ":": ":",
    ";": ";",
    "{": "{",
    "}": "}",
    "[": "[",
    "]": "]",
    "<": "<",
    ">": ">",
    "!": "!",
    "@": "@",
    # "#": "#",
    "$": "$",
    "%": "%",
    "^": "^",
    "&": "&",
    "_": "_",
    "-": "-",
    "+": "+",
    "=": "=",
    "|": "|",
    "\\": "\\",
    "/": "/",
    "": "",
    "~": "~",
    "'": "'",
    '"': '"',
    "?": "?",
    " ": " ",
    "\n": "\n",
    "\t": "\t",
    "\r": "\r",
    "\b": "\b",
    "\f": "\f",
    "\v": "\v",
    "\a": "\a",
    "\0": "\0",
    "\x00": "\x00",
    "\u0000": "\u0000",
    "\U00000000": "\U00000000",
    "\N{NULL}": "\N{NULL}",
}

# Lowercase runes
lowercase_runes = {
    "a": "ᚨ",
    "b": "ᛒ",
    "c": "ᚲ",
    "d": "ᚦ",
    "e": "ᛅ",
    "f": "ᚠ",
    "g": "ᛞ",
    "h": "ᚺ",
    "i": "ᛁ",
    "j": "ᚴ",
    "k": "ᛘ",
    "l": "ᛐ",
    "m": "ᛖ",
    "n": "ᚾ",
    "o": "ᛜ",
    "p": "ᛩ",
    "q": "ᛶ",
    "r": "ᛃ",
    "s": "ᛋ",
    "t": "ᛄ",
    "u": "ᚢ",
    "v": "ᛡ",
    "w": "ᚳ",
    "x": "×",
    "y": "ᛣ",
    "z": "ᛇ",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "0": "0",
    "(": "(",
    ")": ")",
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "=": "=",
    ",": ",",
    ".": ".",
    ":": ":",
    ";": ";",
    "{": "{",
    "}": "}",
    "[": "[",
    "]": "]",
    "<": "<",
    ">": ">",
    "!": "!",
    "@": "@",
    # "#": "#",
    "$": "$",
    "%": "%",
    "^": "^",
    "&": "&",
    "_": "_",
    "-": "-",
    "+": "+",
    "=": "=",
    "|": "|",
    "\\": "\\",
    "/": "/",
    "": "",
    "~": "~",
    "'": "'",
    '"': '"',
    "?": "?",
    " ": " ",
    "\n": "\n",
    "\t": "\t",
    "\r": "\r",
    "\b": "\b",
    "\f": "\f",
    "\v": "\v",
    "\a": "\a",
    "\0": "\0",
    "\x00": "\x00",
    "\u0000": "\u0000",
    "\U00000000": "\U00000000",
    "\N{NULL}": "\N{NULL}",
}

keyword_runes = {
    "var": "𖤍",
    "fun": "♅",
    "if": "↟↟",
    "else": "↟↡",
    "while": "↟↠",
    "for": "𒌐",
    "return": "↡",
    "and": "↠↠",
    "class": "🕈",
    "false": "☽",
    "null": "☽𖤍",
    "pr": "↞↞",
    "print": "♅♅",
    "super": "🕈↟",
    "this": "🕈↡",
    "true": "𖤓",
}

# Create the inverse mappings from custom symbols to alphabet letters
inverse_uppercase_runes = {v: k for k, v in uppercase_runes.items()}
inverse_lowercase_runes = {v: k for k, v in lowercase_runes.items()}
inverse_keyword_runes = {v: k for k, v in keyword_runes.items()}



def translateKeywords(input):
    input = input + " "
    output = []
    word = ""

    for x in input:
        if x == " ":
            if word in inverse_keyword_runes:
                word = inverse_keyword_runes[word]
            output.append(word)
            word = ""
        else:
            word = word + x
    output.append(word)

    return " ".join(output)

def to_custom_symbols(text):
    result = []
    inside_quotes = False
    quote_char = None
    inside_comment = False

    i = 0
    while i < len(text):
        char = text[i]

        # Check if the character is inside quotes
        if char in ('"', "'"):
            if inside_quotes and char == quote_char and (i == 0 or text[i - 1] != "\\"):
                inside_quotes = False
                quote_char = None
            elif not inside_quotes:
                inside_quotes = True
                quote_char = char
            result.append(char)

        # Check for single-line comment
        elif text[i : i + 2] == "//" and not inside_quotes:
            inside_comment = True
            result.append("//")
            i += 1  # Skip the next character
        elif inside_comment:
            if char == "\n":
                inside_comment = False
            result.append(char)

        # Handle keywords by reading whole words
        elif char.isalpha() and not inside_quotes and not inside_comment:
            start = i
            while i < len(text) and text[i].isalpha():
                i += 1
            word = text[start:i]
            if word in keyword_runes:
                result.append(keyword_runes[word])
            else:
                result.append(word)
            continue  # Skip the increment at the end since i is already updated

        # Convert individual characters
        elif char in uppercase_runes:
            result.append(uppercase_runes[char])
        elif char in lowercase_runes:
            result.append(lowercase_runes[char])
        else:
            result.append(char)

        i += 1

    return "".join(result)


def from_custom_symbols(text):
    result = []
    inside_quotes = False
    quote_char = None
    inside_comment = False

    i = 0
    while i < len(text):
        char = text[i]

        # Handle quoted strings
        if char in ('"', "'"):
            if inside_quotes and char == quote_char:
                inside_quotes = False
                quote_char = None
            else:
                inside_quotes = True
                quote_char = char
            result.append(char)

        # Handle single-line comments
        elif text[i : i + 2] == "//" and not inside_quotes:
            inside_comment = True
            result.append("//")
            i += 1
        elif inside_comment:
            if char == "\n":
                inside_comment = False
            result.append(char)

        # Handle multi-character symbols
        else:
            # Attempt to match multi-character symbols for keywords
            matched = False
            for symbol, keyword in sorted(inverse_keyword_runes.items(), key=lambda x: len(x[0]), reverse=True):
                if text[i : i + len(symbol)] == symbol:
                    result.append(keyword)
                    i += len(symbol) - 1  # Skip the matched symbol
                    matched = True
                    break

            # If no multi-character symbol matched, handle single characters
            if not matched:
                if char in inverse_uppercase_runes:
                    result.append(inverse_uppercase_runes[char])
                elif char in inverse_lowercase_runes:
                    result.append(inverse_lowercase_runes[char])
                else:
                    result.append(char)

        i += 1

    return "".join(result)


def convert_valkyrie_to_runic(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    converted_content = to_custom_symbols(content)
    new_filename = filepath.replace(".valkyrie", ".runic")

    if os.path.exists(new_filename):
        os.remove(new_filename)

    with open(new_filename, "w", encoding="utf-8") as f:
        f.write(converted_content)
    print(f"Converted {filepath} to {new_filename}")


def convert_runic_to_valkyrie(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    converted_content = from_custom_symbols(content)
    new_filename = filepath.replace(".runic", ".valkyrie")

    if os.path.exists(new_filename):
        os.remove(new_filename)

    with open(new_filename, "w", encoding="utf-8") as f:
        f.write(converted_content)
    print(f"Converted {filepath} to {new_filename}")


def process_string(input_string):
    converted_string = from_custom_symbols(input_string)
    print(converted_string)


def main():
    parser = argparse.ArgumentParser(
        description="Convert between different file types or process strings."
    )

    # Adding options
    parser.add_argument("-f", "--file", help="The file to convert")
    parser.add_argument("-s", "--string", help="A raw string to process")
    parser.add_argument("-c", "--convert", help="Convert the file", action="store_true")

    args = parser.parse_args()

    # Handle file conversion
    if args.file:
        if not os.path.isfile(args.file):
            print(f"File {args.file} does not exist.")
            return
        elif args.file.endswith(".valkyrie"):
            convert_valkyrie_to_runic(args.file)
        elif args.file.endswith(".runic"):
            convert_runic_to_valkyrie(args.file)
        else:
            print("Invalid file extension for conversion")

    # Handle string processing
    elif args.string:
        # if args.run:
        process_string(args.string)
        # else:
        #     print("Please specify an action for the string: -r to run.")

    else:
        print(
            "Please provide a valid option: -f for file or -s for string, -c for conversion, -r for running."
        )


if __name__ == "__main__":
    main()
