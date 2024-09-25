# Valkyrie Interpreter

Valkyrie Interpreter is a Rust-based interpreter for the Valkyrie programming language, a modification of the language created by [CodeScope](https://gitlab.com/codescope-reference/cii). This interpreter includes the ability to read and translate runes, making it a unique tool for developers interested in working with runic symbols.

## Prerequisites

To use the Valkyrie Interpreter, you need the Valkyrie-Keymap app. This app provides the necessary key mappings for the runic symbols used in the Valkyrie language.

## Features

- **Runic Symbol Support**: Translate and interpret runic symbols in your code.
- **Inheritance**: Classes can inherit from other classes using the `Super` keyword.
- **Classes and Methods**: Define classes and methods with ease.
- **Loops**: Support for `while` and `for` loops.
- **Functions**: Declare functions using the `fun` keyword.
- **Block-Level Scoping**: Supports block-level scoping for variables.
- **Generics**: Use generic types for functions and classes.
- **Getters and Setters**: Encapsulate properties with getters and setters.
- **Pipes**: Chain function calls using pipe operations.
- **Non-Trivial Constructors**: Initialize classes with constructors that accept parameters.
- **This Keyword**: Refer to the current instance of a class using the `This` keyword.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/fram446742/valkyrie-interpreter.git
    ```

2. Navigate to the project directory:

    ```sh
    cd valkyrie-rust
    ```

3. Build the project using Cargo:

    ```sh
    cargo build --release
    ```

## Usage

### Running a File

To run a Valkyrie file, use the following command:

```sh
cargo run --release run_file <path_to_file>
```

### Interactive Prompt

To start an interactive prompt:

```sh
cargo run --release run_prompt
```

### Runic Prompt

To start a runic interactive prompt:

```sh
cargo run --release run_prompt_runic
```

### Compiling a File

```sh
cargo run --release compile_file <path_to_file>
```

## Documentation

Please refer to the [documentation](DOCUMENTATION.md) file.

## Example

Here is an example of a Valkyrie program:

```valkyrie
𒌐 (𖤍 = 0; 𖤍 < 10; 𖤍 = 𖤍 + 1) {
    ♅♅(𖤍);
}
```

This code will print numbers from 0 to 9.

## License

This project is licensed under the GNU License.

## Acknowledgements

- [CodeScope](https://gitlab.com/codescope-reference/cii) for the original language design.
- The Rust community for their support and contributions.

For more information, please refer to the original [code](https://gitlab.com/codescope-reference/cii).
