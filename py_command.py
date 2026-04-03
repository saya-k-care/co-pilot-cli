import subprocess
import sys
import argparse

# --- Configuration ---
# Note: 'gh copilot' usually requires a subcommand like 'suggest' or 'explain'
DEFAULT_COMMAND = ["gh copilot", "-i", '"who are u in 20 words. Print program copilot executed successfully"', "--allow-all"]

parser = argparse.ArgumentParser(
    description="Run a shell command, log output, and terminate on success keyword."
)

parser.add_argument(
    "command", 
    nargs="*", 
    default=DEFAULT_COMMAND,
    help="The shell command to execute (defaults to gh copilot if empty)"
)

parser.add_argument(
    "--success-keyword",
    default="successfully",
    help="Keyword to detect successful completion",
)
parser.add_argument(
    "--log-file",
    default="command_output.log",
    help="Log file path",
)
args = parser.parse_args()

def run_command(command, success_keyword, log_file):
    """
    Executes a command, logs output to a file, and terminates if a specific keyword is found.
    """
    print("=" * 40)
    print("🚀 EXECUTION PARAMETERS")
    # Join command list into a string for display and shell execution
    cmd_string = " ".join(command) if isinstance(command, list) else command
    print(f"🔹 Full Command: {cmd_string}")
    print(f"🔹 Success Key:  '{success_keyword}'")
    print(f"🔹 Log File:     {log_file}")
    print("=" * 40 + "\n")

    try:
        with open(log_file, "w", encoding="utf-8") as log:
            # Using shell=True is often necessary on Windows for 'gh' or 'npm' commands
            process = subprocess.Popen(
                cmd_string,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                shell=True 
            )

            print("[*] Process started. Monitoring stream...\n")

            if process.stdout:
                for line in process.stdout:
                    log.write(line)
                    log.flush()
                    print(line, end="")

                    if success_keyword.lower() in line.lower():
                        print(f"\n\n✅ Detected success keyword '{success_keyword}'. Terminating.")
                        process.terminate()
                        return True

            process.wait()

            if process.returncode == 0:
                print("\n✅ Command completed naturally.")
                return True
            else:
                print(f"\n❌ Exit code {process.returncode}. Check {log_file}")
                return False

    except FileNotFoundError:
        print(f"❌ Error: The command '{command[0]}' was not found. Is it in your PATH?")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    success = run_command(args.command, args.success_keyword, args.log_file)
    sys.exit(0 if success else 1)