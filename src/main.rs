mod environment;
mod expr;
mod interpreter;
mod parser;
mod resolver;
mod scanner;
mod stmt;
mod tests;
use crate::interpreter::*;
use crate::parser::*;
use crate::resolver::*;
use crate::scanner::*;
use std::fs;
use std::fs::File;
use std::io::Cursor;
use std::io::{self, BufRead, Write};
use std::path::Path;
use std::process::exit;
use zip::ZipArchive;

pub fn run_file(path: &str) -> Result<(), String> {
    // let mut interpreter = Interpreter::new();
    match fs::read_to_string(path) {
        Err(msg) => return Err(msg.to_string()),
        Ok(contents) => return run_string(&contents),
    }
}

pub fn run_string(contents: &str) -> Result<(), String> {
    let mut interpreter = Interpreter::new();

    run(&mut interpreter, contents)
}

fn run(interpreter: &mut Interpreter, contents: &str) -> Result<(), String> {
    let mut scanner = Scanner::new(contents);
    let tokens = scanner.scan_tokens()?;

    let mut parser = Parser::new(tokens);
    let stmts = parser.parse()?;

    let resolver = Resolver::new();
    let locals = resolver.resolve(&stmts.iter().collect())?;

    interpreter.resolve(locals);

    interpreter.interpret(stmts.iter().collect())?;
    return Ok(());
}

fn run_prompt(stdout: &mut io::Stdout, stdin: &mut io::Stdin) -> Result<(), String> {
    let mut interpreter = Interpreter::new();
    loop {
        println!("Running in prompt mode - simply press enter to exit");
        print!("> ");
        match stdout.flush() {
            Ok(_) => (),
            Err(_) => return Err("Could not flush stdout".to_string()),
        }

        let mut buffer = String::new();
        // let stdin = io::stdin();
        let mut handle = stdin.lock();
        match handle.read_line(&mut buffer) {
            Ok(n) => {
                if buffer.trim().is_empty() {
                    println!("");
                    return Ok(());
                } else if n == 1 {
                    continue;
                }
            }
            Err(_) => return Err("Couldnt read line".to_string()),
        }

        println!("ECHO: {}", buffer);
        match run(&mut interpreter, &buffer) {
            Ok(_) => (),
            Err(msg) => println!("{}", msg),
        }
    }
}

fn run_prompt_runic(
    stdout: &mut io::Stdout,
    stdin: &mut io::Stdin,
    python_script: &[u8],
) -> Result<(), String> {
    let mut interpreter = Interpreter::new();
    loop {
        println!("Running in prompt mode (Runic) - simply press enter to exit");
        println!("WARNING: In this mode custom characters are not supported");
        print!("> ");
        match stdout.flush() {
            Ok(_) => (),
            Err(_) => return Err("Could not flush stdout".to_string()),
        }

        let mut buffer = String::new();
        // let stdin = io::stdin();
        let mut handle = stdin.lock();
        match handle.read_line(&mut buffer) {
            Ok(n) => {
                if buffer.trim().is_empty() {
                    println!("");
                    return Ok(());
                } else if n == 1 {
                    continue;
                }
            }
            Err(_) => return Err("Couldnt read line".to_string()),
        }

        // Call Python function to convert the input
        let converted_buffer = match convert_input_with_python(&buffer, python_script) {
            Ok(result) => result,
            Err(msg) => {
                println!("Error during conversion: {}", msg);
                continue;
            }
        };

        println!("Converted: {}", converted_buffer);
        match run(&mut interpreter, &converted_buffer) {
            Ok(_) => (),
            Err(msg) => println!("{}", msg),
        }
    }
}

fn convert_input_with_python(input: &str, python_script: &[u8]) -> Result<String, String> {
    let mut temp_file = std::env::temp_dir();
    temp_file.push("runic-compiler.py");

    if let Err(_) = fs::write(&temp_file, python_script) {
        return Err("Could not write temporary Python script".to_string());
    }

    let output = std::process::Command::new("python")
        .arg(temp_file.to_str().unwrap())
        .arg("-s")
        .arg(input.to_string()) // Pass the input to the Python script
        .output();

    match output {
        Ok(output) => {
            if output.status.success() {
                let converted_string = String::from_utf8_lossy(&output.stdout).trim().to_string();
                Ok(converted_string)
            } else {
                Err(format!(
                    "Python script failed with error: {}",
                    String::from_utf8_lossy(&output.stderr)
                ))
            }
        }
        Err(e) => Err(format!("Failed to execute Python script: {}", e)),
    }
}

fn display_menu() {
    println!("Select an option:");
    println!("1. Run a file");
    println!("2. Run a string");
    println!("3. Run in prompt mode");
    println!("4. Run in prompt mode (Runic)");
    println!("5. Compile only");
    println!("6. Show help");
    println!("7. Exit");
    print!("> ");
}

fn get_user_input(stdout: &mut io::Stdout) -> String {
    if let Err(_) = stdout.flush() {
        println!("Could not flush stdout");
    }

    let mut buffer = String::new();
    let stdin = io::stdin();
    let mut handle = stdin.lock();
    if let Err(_) = handle.read_line(&mut buffer) {
        println!("Could not read line");
    }
    buffer
}

fn run_file_option(stdout: &mut io::Stdout, python_script: &[u8]) {
    let file_path = get_file_path(stdout);

    let valkyrie: String;
    match file_path {
        ref path if path.ends_with(".runic") => {
            compile_python_script(path.clone(), python_script);
            valkyrie = file_path.replace(".runic", ".valkyrie");
        }
        ref path if path.ends_with(".valkyrie") => {
            valkyrie = path.clone();
        }
        _ => {
            println!("Error: File path must end with .runic or .valkyrie");
            return;
        }
    }

    // if !file_path.ends_with(".runic") {
    //     println!("Error: File path must end with .runic");
    //     return;
    // }

    match run_file(&valkyrie.trim()) {
        Ok(_) => println!("File executed successfully"),
        Err(msg) => println!("ERROR:\n{}", msg),
    }
}

fn run_string_option(stdout: &mut io::Stdout) {
    print!("Enter string to run: ");
    if let Err(_) = stdout.flush() {
        println!("Could not flush stdout");
        return;
    }

    let mut input_string = String::new();
    let stdin = io::stdin();
    let mut handle = stdin.lock();
    if let Err(_) = handle.read_line(&mut input_string) {
        println!("Could not read line");
        return;
    }

    match run_string(input_string.trim()) {
        Ok(_) => println!("String executed successfully"),
        Err(msg) => println!("ERROR:\n{}", msg),
    }
}

fn run_prompt_option(stdout: &mut io::Stdout) {
    let mut stdin = io::stdin();
    match run_prompt(stdout, &mut stdin) {
        Ok(_) => println!("Exited prompt mode"),
        Err(msg) => println!("ERROR\n{}", msg),
    }
}

fn run_prompt_option_runic(stdout: &mut io::Stdout, python_script: &[u8]) {
    let mut stdin = io::stdin();
    match run_prompt_runic(stdout, &mut stdin, python_script) {
        Ok(_) => println!("Exited prompt mode"),
        Err(msg) => println!("ERROR\n{}", msg),
    }
}

fn compile_only_option(stdout: &mut io::Stdout, python_script: &[u8]) {
    let file_path = get_file_path(stdout);

    if !file_path.ends_with(".runic") {
        println!("Error: File path must end with .runic");
        return;
    }

    compile_python_script(file_path.clone(), python_script);
    println!("File compiled to Valkyrie format");
}

fn get_file_path(stdout: &mut io::Stdout) -> String {
    print!("Enter file path: ");
    if let Err(_) = stdout.flush() {
        println!("Could not flush stdout");
    }

    let mut file_path = String::new();
    let stdin = io::stdin();
    let mut handle = stdin.lock();
    if let Err(_) = handle.read_line(&mut file_path) {
        println!("Could not read line");
    }

    file_path.trim().to_string()
}

fn compile_python_script(file_path: String, python_script: &[u8]) {
    let mut temp_file = std::env::temp_dir();
    temp_file.push("runic-compiler.py");

    if let Err(_) = fs::write(&temp_file, python_script) {
        println!("Could not write temporary Python script");
        return;
    }

    let output = std::process::Command::new("python")
        .arg(temp_file.to_str().unwrap())
        .arg("-f")
        .arg(file_path.trim())
        .output()
        .expect("Failed to execute python script");

    if let Err(_) = fs::remove_file(&temp_file) {
        println!("Warning: Could not remove temporary Python script");
    }

    if !output.status.success() {
        println!(
            "Python script failed with error: {}",
            String::from_utf8_lossy(&output.stderr)
        );
    }
}

fn main() {
    let python_script: &[u8] = include_bytes!("py/runic-compiler.py");
    let test_folder: &[u8] = include_bytes!("examples/examples.zip");
    // let HELP = include_bytes!("help.txt");

    let args: Vec<String> = std::env::args().collect();

    if args.len() > 1 {
        let mut stdout = io::stdout();
        match args[1].as_str() {
            "run_file" => {
                if args.len() < 3 {
                    println!("Usage: run_file <file_path>");
                    return;
                }
                run_file_option(&mut stdout, python_script);
            }
            "run_string" => {
                if args.len() < 3 {
                    println!("Usage: run_string <string>");
                    return;
                }
                run_string_option(&mut stdout);
            }
            "run_prompt" => run_prompt_option(&mut stdout),
            "run_prompt_runic" => run_prompt_option_runic(&mut stdout, python_script),
            "compile_file" => {
                if args.len() < 3 {
                    println!("Usage: compile_file <file_path>");
                    return;
                }
                compile_only_option(&mut stdout, python_script);
            }
            "help" => run_help(&mut stdout, test_folder),
            _ => println!("Invalid argument, please try again"),
        }
        return;
    }

    loop {
        display_menu();

        let mut stdout = io::stdout();
        let buffer = get_user_input(&mut stdout);

        match buffer.trim() {
            "1" => run_file_option(&mut stdout, python_script),
            "2" => run_string_option(&mut stdout),
            "3" => run_prompt_option(&mut stdout),
            "4" => run_prompt_option_runic(&mut stdout, python_script),
            "5" => compile_only_option(&mut stdout, python_script),
            "6" => {
                run_help(&mut stdout, test_folder);
            }
            "7" => {
                println!("Exiting...");
                exit(0);
            }
            _ => println!("Invalid option, please try again"),
        }
    }
}

fn run_help(stdout: &mut io::Stdout, test_folder: &[u8]) {
    println!("Valkyrie Interpreter");
    println!("This is a simple interpreter for the Valkirie language.");
    println!("Valkirie is a simple language that is designed to be easy to learn and use.");
    println!("It has the capability to run using both runes and Latin characters.");
    println!("It is a dynamically typed language with a simple syntax.");
    println!("The interpreter is written in Rust and uses a Python script to convert Runic code to Valkyrie code.");
    println!("The interpreter can run Runic code from a file, a string, or in prompt mode.");
    println!("In prompt mode, you can enter Runic code line by line.");
    println!("The interpreter can also compile Runic code to Valkyrie code without running it.");
    println!("Test cases are included in the binary.");

    print!("Do you want to decompress the examples? (y/n): ");
    if stdout.flush().is_err() {
        println!("Could not flush stdout");
        return;
    }

    let mut buffer = String::new();
    let stdin = io::stdin();
    let mut handle = stdin.lock();
    if handle.read_line(&mut buffer).is_err() {
        println!("Could not read line");
        return;
    }

    if buffer.trim().eq_ignore_ascii_case("y") {
        decompress_examples(test_folder);
    }
}

fn decompress_examples(test_folder: &[u8]) {
    let reader = Cursor::new(test_folder);
    let mut archive = match ZipArchive::new(reader) {
        Ok(archive) => archive,
        Err(e) => {
            println!("Error reading zip archive: {}", e);
            return;
        }
    };

    let output_dir = Path::new("examples");

    // Create the examples directory if it doesn't exist
    if std::fs::create_dir_all(&output_dir).is_err() {
        println!("Could not create 'examples' directory");
        return;
    }

    // Extract each file from the archive
    for i in 0..archive.len() {
        let mut file = match archive.by_index(i) {
            Ok(file) => file,
            Err(e) => {
                println!("Error accessing file in zip: {}", e);
                return;
            }
        };

        let outpath = match file.enclosed_name() {
            Some(path) => output_dir.join(path),
            None => continue,
        };

        // Create directories if the file is inside a folder
        if file.name().ends_with('/') {
            if std::fs::create_dir_all(&outpath).is_err() {
                println!("Could not create directory for {}", outpath.display());
                return;
            }
        } else {
            let mut outfile = match File::create(&outpath) {
                Ok(f) => f,
                Err(e) => {
                    println!("Error creating file {}: {}", outpath.display(), e);
                    return;
                }
            };

            if std::io::copy(&mut file, &mut outfile).is_err() {
                println!("Error writing to file {}", outpath.display());
                return;
            }
        }

        // Set file permissions if needed
        #[cfg(unix)]
        if let Some(mode) = file.unix_mode() {
            let _ = std::fs::set_permissions(&outpath, std::fs::Permissions::from_mode(mode));
        }

        // println!("Extracted {}", outpath.display());
    }

    println!("Examples decompressed successfully.");
}
