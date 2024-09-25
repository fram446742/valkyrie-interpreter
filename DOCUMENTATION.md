
# Documentation

## Syntax and Semantics

### Syntactic Rules

- Every statement ends with a semicolon `;`.
- Comments are indicated with `//`.
- Variable declaration:

  ```valkyrie
  var <name> = <value>;
  ```

- Multiple variable declarations:

  ```valkyrie
  { var <name1> = <value1>; var <name2> = <value2>; ... }
  ```

- Printing variables:

  ```valkyrie
  print <variable>;
  ```

### Classes and Inheritance

- Defining a class:

  ```valkyrie
  class <Name> {
      ...
  }
  ```

- Class inheritance:

  ```valkyrie
  class <Child> < <Parent> {
      ...
  }
  ```

- Defining methods in a class:

  ```valkyrie
  class <Name> {
      method(param1, param2, ...) {
          ...
      }
  }
  ```

- Calling a method:

  ```valkyrie
  <class>.method(args);
  ```

- Defining the constructor method `init()`:

  ```valkyrie
  class <Name> {
      init() {
          this.<attribute> = ...;
      }
  }
  ```

- Constructor with inheritance:

  ```valkyrie
  class <Child> < <Parent> {
      init() {
          super.init();
      }
  }
  ```

### Control Structures

- Conditional statements:

  ```valkyrie
  if (<condition>) {
      ...
  }
  ```

- `for` loop:

  ```valkyrie
  for (var = <initialization>; <condition>; <increment>) {
      ...
  }
  ```

- `while` loop:

  ```valkyrie
  while (<condition>) {
      ...
  }
  ```

### Functions

- Defining a function:

  ```valkyrie
  fun <name> (params) {
      ...
      return <value>;
  }
  ```

  If no return value is defined, the function will return `null` by default.

- Using variables with functions:

  - Declaration:

    ```valkyrie
    var <name> = <function>();
    ```

  - Function call:

    ```valkyrie
    <name>();
    ```

- The language supports "pipes" to pass dynamic arguments into functions. Example:

  ```valkyrie
  var <variable> = <value> |> <fun>;
  ```

### Semantic Rules

- Inheriting from something that is not a class or self-inheritance will result in an error.
- Functions that do not return an explicit value will return `null`.

## Code Style

Instead of traditional keywords, Valkyrie uses symbols for various operations:

- `var = 𖤍`: Variable declaration.
- `fun = ♅`: Function declaration.
- `if = ↟↟`: Conditional *if*.
- `else = ↟↡`: Conditional *else*.
- `while = ↟↠`: *while* loop.
- `for = 𒌐`: *for* loop.
- `return = ↡`: Function return.
- `and = ↠↠`: Logical *AND* operator.
- `class = 🕈`: Class definition.
- `false = ☽`: Boolean *false*.
- `null = ☽𖤍`: Null value.
- `or = ↞↞`: Logical *OR* operator.
- `print = ♅♅`: Print statement.
- `super = 🕈↟`: Reference to the superclass.
- `this = 🕈↡`: Reference to the current instance.
- `true = 𖤓`: Boolean *true*.

## Debugging and Error Handling

Errors in Valkyrie are handled by the interpreter, which returns messages indicating issues such as syntax or semantic errors, including poorly defined inheritance or functions without explicit return values.

## Usage Examples

**To be added**

## Versioning and Updates

This document will be updated as the language evolves.
