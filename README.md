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
git clone https://github.com/Dorlinrozin/ocs01-test.git
cd ocs01-test
cargo build --release
```

**Copy json file**

```bash
cp EI/exec_interface.json .
```

**required files in same directory**

-   wallet.json - create with your credentials
-   exec_interface.json - copy from EI/ folder

you need your `wallet.json` file which has your wallet details like the last time in "octra_pre_client" dir
```bash
cd octra_pre_client
```
```bash
cp ./wallet.json ../ocs01-test
cd ../ocs01-test
```
if you can't locate `wallet.json` file, just create one in `ocs01-test` dir
```bash
nano wallet.json
```
copy and edit
```bash
{
  "priv": "PRIVATE_KEY",
  "addr": "ADDRESS",
  "rpc": "https://octra.network"
}
```
press `Ctrl+X`, press `y`, then press `Enter` to save

copy `EI/exec_interface.json` file to `ocs01-test`. use the following command
```bash
cp EI/exec_interface.json .
```

## ▶️ **How to Run**

Make a Screen
```bash
screen -S automator
```
Execute the Python script:
```bash
python3 menu_automator.py 
```
Enter the number of times to repeat the test cycle and the delay in seconds between each cycle

After running successfully close from screen with pressing `Ctrl A+D`

*for this task the ei file contains the interface for contract at address octBUHw585BrAMPMLQvGuWx4vqEsybYH9N7a3WNj1WBwrDn, do not modify it*

after running, follow the menu to interact with the contract
