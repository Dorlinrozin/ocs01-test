# ===== IMPORTS & DEPENDENCIES =====
import pexpect
import json
import time
import sys
import re
import random

class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'

# ===== HELPER FUNCTION =====

def generate_params_for_method(method):
    """
    Generates more intelligent and varied parameters for automated testing
    to avoid common mathematical errors like division by zero.
    """
    params_data = []
    # Use a set to track values used for specific parameters to ensure uniqueness
    used_values = set()

    for param in method.get("params", []):
        param_type = param.get("type")
        param_name = param.get("name")
        
        if param_type == "address":
            params_data.append(param.get("example", "octXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"))
        elif param_type == "number":
            value = 0
            # --- Specific logic for linearInterpolate to avoid division by zero ---
            if method["name"] == "linearInterpolate" and param_name == "x1":
                # Ensure x1 is different from x0. We assume x0 was the previous param.
                x0_val = int(params_data[-1]) if params_data else 0
                value = x0_val + 5 # Just pick a different number
                while value in used_values:
                    value += 1
            else:
                # General logic for other number parameters
                if "max" in param:
                    # Pick a random number between 1 and a safe upper bound
                    upper_bound = min(int(param["max"]), 20)
                    value = random.randint(1, upper_bound)
                else:
                    # Pick a random number
                    value = random.randint(1, 15)
                
                # Ensure the generated value is not already used in this method call
                while value in used_values:
                    value = random.randint(1, 20)
            
            used_values.add(value)
            params_data.append(str(value))
            
    return params_data

def run_test_cycle(cycle_number, total_cycles):
    """Runs a single full test cycle, now robust against ANSI color codes."""
    command = "./target/release/ocs01-test"
    try:
        with open("exec_interface.json", "r") as f:
            interface = json.load(f)
    except FileNotFoundError as e:
        print(f"{colors.RED}Error: {e}. Make sure 'exec_interface.json' is present.{colors.ENDC}")
        return False

    print(f"\n{colors.CYAN}========== Starting Test Cycle {cycle_number} of {total_cycles} =========={colors.ENDC}")
    
    try:
        child = pexpect.spawn(command, encoding='utf-8', timeout=45)
        # It's helpful to see the raw, uncolored output for debugging.
        # Set the logfile to sys.stdout to see exactly what pexpect sees.
        child.logfile_read = sys.stdout
        
    except pexpect.exceptions.ExceptionPexpect as e:
        print(f"{colors.RED}Failed to start the process '{command}'. Error: {e}{colors.ENDC}")
        return False

    try:
        # Define patterns using regular expressions to ignore color codes
        CHOICE_PROMPT = re.compile(r"choice:\s*")
        CONTINUE_PROMPT = re.compile(r"press enter to continue\.\.\.")
        RESULT_PATTERN = re.compile(r"result: (.*)")
        CONFIRM_PROMPT = re.compile(r"wait for confirmation\? y/n:\s*")
        
        child.expect(CHOICE_PROMPT)
        initial_output = child.before
        print(initial_output.strip())

        for i, method in enumerate(interface["methods"]):
            menu_choice = str(i + 1)
            method_label = method["label"]
            
            print(f"{colors.BLUE}--- Testing '{method_label}' (Option {menu_choice}) ---{colors.ENDC}")
            child.sendline(menu_choice)
            
            method_header_pattern = re.compile(f"--- {re.escape(method['name'])} ---")
            child.expect(method_header_pattern)

            params_to_send = generate_params_for_method(method)
            for param_value in params_to_send:
                child.expect(r":\s*")
                child.sendline(param_value)
                print(f"   - Input: Sent '{param_value}'")

            if method["type"] == "view":
                child.expect(RESULT_PATTERN)
                # The result is in the first captured group of the match
                result = child.match.group(1).strip()
                # Clean up any remaining ANSI codes from the result string itself
                clean_result = re.sub(r'\x1b\[[0-9;]*m', '', result)
                print(f"   {colors.GREEN}✔ Result: {clean_result}{colors.ENDC}")
                child.expect(CONTINUE_PROMPT)

            elif method["type"] == "call":
                child.expect(CONFIRM_PROMPT)
                child.sendline("y")
                print("   - Action: Confirmed waiting for transaction.")
                
                # We expect the plain text, as the color codes will be stripped by pexpect's matching
                status_patterns = [re.compile(r"confirmed"), re.compile(r"timeout"), re.compile(r"error:")]
                index = child.expect(status_patterns, timeout=120)

                if index == 0:
                    print(f"   {colors.GREEN}✔ Status: Confirmed{colors.ENDC}")
                else:
                    print(f"   {colors.RED}✖ Status: Failed or Timed Out{colors.ENDC}")
                
                child.expect(CONTINUE_PROMPT)
            
            child.sendline("") # Send 'Enter' to go back to main menu
            child.expect(CHOICE_PROMPT)
            time.sleep(2)
        
        child.sendline("0") # Exit
        child.expect("bye")
        child.close()
        print(f"\n{colors.GREEN}========== Test Cycle {cycle_number} Completed Successfully =========={colors.ENDC}")
        return True

    except pexpect.exceptions.ExceptionPexpect as e:
        print(f"\n{colors.RED}An error occurred during interaction in cycle {cycle_number}.{colors.ENDC}")
        print(f"Error details: {e}")
        print(f"\n{colors.YELLOW}--- Process Buffer Before Error ---")
        print(child.before)
        print("---------------------------------{colors.ENDC}")
        return False
    finally:
        # Deactivate logging to prevent printing after this function
        child.logfile_read = None
        if child.isalive():
            child.terminate()

# ===== MAIN EXECUTION LOGIC =====

def main():
    """Main function to get user input and run test cycles."""
    print(f"{colors.BLUE}--- Automated Test Suite for ocs01 ---{colors.ENDC}")
    
    # --- Get user input for test configuration ---
    while True:
        try:
            num_repeats = int(input(f"{colors.YELLOW}Enter the number of times to repeat the test cycle: {colors.ENDC}"))
            if num_repeats > 0:
                break
            else:
                print(f"{colors.RED}Please enter a positive number.{colors.ENDC}")
        except ValueError:
            print(f"{colors.RED}Invalid input. Please enter a number.{colors.ENDC}")
            
    while True:
        try:
            delay_seconds = int(input(f"{colors.YELLOW}Enter the delay in seconds between each cycle: {colors.ENDC}"))
            if delay_seconds >= 0:
                break
            else:
                print(f"{colors.RED}Please enter a non-negative number.{colors.ENDC}")
        except ValueError:
            print(f"{colors.RED}Invalid input. Please enter a number.{colors.ENDC}")

    # --- Run the test cycles ---
    for i in range(1, num_repeats + 1):
        success = run_test_cycle(i, num_repeats)
        if not success:
            print(f"{colors.RED}Stopping test suite due to an error in the last cycle.{colors.ENDC}")
            break
        
        if i < num_repeats:
            print(f"\n{colors.CYAN}Waiting for {delay_seconds} seconds before the next cycle...{colors.ENDC}")
            time.sleep(delay_seconds)
            
    print(f"\n{colors.BLUE}--- Test Suite Finished ---{colors.ENDC}")

if __name__ == "__main__":
    main()
