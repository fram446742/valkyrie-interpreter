import io
import os
import sys
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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
    "And": "↠↠",
    "Class": "🕈",
    "False": "☽",
    "Null": "☽𖤍",
    "Or": "↞↞",
    "Print": "♅♅",
    "Super": "🕈↟",
    "This": "🕈↡",
    "True": "𖤓",
}

# Create the inverse mappings from custom symbols to alphabet letters
inverse_uppercase_runes = {v: k for k, v in uppercase_runes.items()}
inverse_lowercase_runes = {v: k for k, v in lowercase_runes.items()}
inverse_keyword_runes = {v: k for k, v in keyword_runes.items()}


def to_custom_symbols(text, is_rust=False):
    result = []
    inside_quotes = False
    quote_char = None
    inside_comment = False
    inside_block_comment = False

    i = 0
    while i < len(text):
        char = text[i]

        # Handle Rust block comments /* ... */
        if (
            is_rust
            and not inside_quotes
            and not inside_comment
            and text[i : i + 2] == "/*"
        ):
            inside_block_comment = True
            result.append("/*")
            i += 1  # Skip the next character
        elif is_rust and inside_block_comment and text[i : i + 2] == "*/":
            inside_block_comment = False
            result.append("*/")
            i += 1  # Skip the next character
        elif inside_block_comment:
            result.append(char)

        # Check if the character is inside quotes
        elif char in ('"', "'"):
            if inside_quotes and char == quote_char:
                inside_quotes = False
                quote_char = None
            else:
                inside_quotes = True
                quote_char = char
            result.append(char)

        # Handle Rust line comments starting with //
        elif is_rust and text[i : i + 2] == "//" and not inside_quotes:
            inside_comment = True
            result.append("//")
            i += 1  # Skip the next character
        elif inside_comment:
            if char == "\n":
                inside_comment = False
            result.append(char)

        # Handle Python # comments
        elif not is_rust and char == "#" and not inside_quotes:
            inside_comment = True
            result.append(char)
        elif inside_comment:
            if char == "\n":
                inside_comment = False
            result.append(char)

        # Convert symbols
        # TODO: Handle multi-character keywords
        elif char in uppercase_runes:
            result.append(uppercase_runes[char])
        elif char in lowercase_runes:
            result.append(lowercase_runes[char])
        else:
            result.append(char)

        i += 1
    return "".join(result)


def from_custom_symbols(text, is_rust=False):
    result = []
    inside_quotes = False
    quote_char = None
    i = 0
    inside_comment = False
    inside_block_comment = False

    while i < len(text):
        char = text[i]

        # Handle Rust block comments /* ... */
        if (
            is_rust
            and not inside_quotes
            and not inside_comment
            and text[i : i + 2] == "/*"
        ):
            inside_block_comment = True
            result.append("/*")
            i += 1
        elif is_rust and inside_block_comment and text[i : i + 2] == "*/":
            inside_block_comment = False
            result.append("*/")
            i += 1
        elif inside_block_comment:
            result.append(char)

        # Handle quoted strings
        elif char in ('"', "'"):
            if inside_quotes and char == quote_char:
                inside_quotes = False
                quote_char = None
            else:
                inside_quotes = True
                quote_char = char
            result.append(char)

        # Handle Rust line comments starting with //
        elif is_rust and text[i : i + 2] == "//" and not inside_quotes:
            inside_comment = True
            result.append("//")
            i += 1
        elif inside_comment:
            if char == "\n":
                inside_comment = False
            result.append(char)

        # Handle Python comments
        elif not is_rust and char == "#" and not inside_quotes:
            inside_comment = True
            result.append(char)
        elif inside_comment:
            if char == "\n":
                inside_comment = False
            result.append(char)

        # Handle multi-character keywords
        elif char in keyword_runes:
            keyword = char
            j = i + 1
            while j < len(text) and text[j] in keyword_runes:
                keyword += text[j]
                j += 1
            if keyword in keyword_runes:
                result.append(keyword_runes[keyword])
                i = j - 1
            else:
                result.append(char)

        # Convert symbols back to original
        elif char in inverse_uppercase_runes:
            result.append(inverse_uppercase_runes[char])
        elif char in inverse_lowercase_runes:
            result.append(inverse_lowercase_runes[char])
        elif char in inverse_keyword_runes:
            result.append(inverse_keyword_runes[char])
        else:
            result.append(char)

        i += 1
    return "".join(result)


def convert_py_to_runyc(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    converted_content = to_custom_symbols(content, is_rust=False)
    new_filename = filepath.replace(".py", ".runyc")

    if os.path.exists(new_filename):
        os.remove(new_filename)

    with open(new_filename, "w", encoding="utf-8") as f:
        f.write(converted_content)
    print(f"Converted {filepath} to {new_filename}")


def convert_valkyrie_to_runic(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    converted_content = to_custom_symbols(content, is_rust=True)
    new_filename = filepath.replace(".valkyrie", ".runic")

    if os.path.exists(new_filename):
        os.remove(new_filename)

    with open(new_filename, "w", encoding="utf-8") as f:
        f.write(converted_content)
    print(f"Converted {filepath} to {new_filename}")


def convert_runyc_to_py(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    converted_content = from_custom_symbols(content, is_rust=False)
    new_filename = filepath.replace(".runyc", ".py")

    if os.path.exists(new_filename):
        os.remove(new_filename)

    with open(new_filename, "w", encoding="utf-8") as f:
        f.write(converted_content)
    print(f"Converted {filepath} to {new_filename}")


def convert_runic_to_valkyrie(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    converted_content = from_custom_symbols(content, is_rust=True)
    new_filename = filepath.replace(".runic", ".valkyrie")

    if os.path.exists(new_filename):
        os.remove(new_filename)

    with open(new_filename, "w", encoding="utf-8") as f:
        f.write(converted_content)
    print(f"Converted {filepath} to {new_filename}")


def process_string(input_string):
    converted_string = from_custom_symbols(input_string, is_rust=False)
    print(converted_string)

def main():
    parser = argparse.ArgumentParser(description="Convert between different file types or process strings.")
    
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
        elif args.file.endswith(".py"):
            convert_py_to_runyc(args.file)
        elif args.file.endswith(".valkyrie"):
            convert_valkyrie_to_runic(args.file)
        elif args.file.endswith(".runyc"):
            convert_runyc_to_py(args.file)
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
        print("Please provide a valid option: -f for file or -s for string, -c for conversion, -r for running.")

if __name__ == "__main__":
    main()
