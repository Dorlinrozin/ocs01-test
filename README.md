# OCS01 Python Test Automator

A Python-based automation script to interact with and test the `ocs01-test` Rust CLI. Instead of manually navigating the interactive menu, this script runs the CLI as a subprocess and automates the testing of all smart contract methods defined in `exec_interface.json`.

This project serves as a practical example of controlling interactive command-line applications using Python, specifically designed for the Octra Labs `ocs01-test` challenge.

## 🚀 Features

-   **Fully Automated**: Runs the Rust CLI and interacts with its menu without user intervention.
-   **Dynamic Test Generation**: Automatically reads `exec_interface.json` to discover and test all available smart contract methods.
-   **Intelligent Parameter Generation**: Creates valid test data for methods, avoiding common errors like division-by-zero.
-   **Configurable Cycles**: Allows setting the number of test cycles and the delay between them for stress and endurance testing.
-   **Robust Interaction**: Uses `pexpect` to reliably control the subprocess, handling prompts and outputs, even with ANSI color codes.

## 📋 Prerequisites

-   **Linux or macOS**: The script relies on `pexpect`, which is not available on Windows.
-   **Python 3.6+**
-   The compiled **`ocs01-test` Rust binary** (must be executable).
-   **Required Python libraries**:
    ```bash
    pip install pexpect
    ```

## ⚙️ Setup

**install rust (if not installed)**

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

**build from source**

```bash
git clone https://github.com/Dorlinrozin/ocs01-test-auto.git
cd ocs01-test
cargo build --release
```

**setup**

```bash
# copy contract interface
cp EI/exec_interface.json .
```

**required files in same directory**

-   wallet.json - create with your credentials
-   exec_interface.json - copy from EI/ folder

**run**

you must copy the release binary to your cli folder and also copy the EI file (execution interface file) to the same location 

the release binary is located in this folder after successful build. 
```bash
./target/release/ocs01-test
```

*for this task the ei file contains the interface for contract at address octBUHw585BrAMPMLQvGuWx4vqEsybYH9N7a3WNj1WBwrDn, do not modify it*

after running, follow the menu to interact with the contract
