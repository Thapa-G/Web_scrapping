import subprocess
import sys


def run_script(script_name):
    try:
        python_executable = sys.executable

        subprocess.run([python_executable, script_name], check=True)
        print(f"{script_name} ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")
    except FileNotFoundError:
        print(f"{script_name} not found.")

if __name__ == "__main__":
    print("Running `try10.py`...")
    run_script("try10.py")

    print("\nRunning `csv_converter.py`...")
    run_script("csv_convertor.py")  # Run the CSV converter script

    print("\nAll scripts ran successfully!")
