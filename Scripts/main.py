from pathlib import Path
import subprocess
import sys
import time


def run_script(script_path):
    print()
    print("=" * 80)
    print(f"Running: {script_path}")
    print("=" * 80)

    time_0 = time.time()
    
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=script_path.parent.parent,
    )
    
    time_end = time.time()
    elapsed = time_end - time_0

    if result.returncode != 0:
        raise RuntimeError(f"Script failed: {script_path}")

    print(f"Finished: {script_path}")
    print(f"Time taken: {elapsed} seconds")


def main():
    project_root = Path(__file__).resolve().parent

    scripts = [
        project_root / "jumbo_scraper.py",
        project_root  / "jumbo_interpreter.py",
        project_root  / "plus_scraper.py",
        project_root / "plus_interpreter.py",
        project_root  / "data_cleaner.py",
        project_root  / "save_dataframe_to_database.py",
        project_root  / "generate_report.py",
    ]

    for script_path in scripts:
        run_script(script_path)

    print()
    print("=" * 80)
    print("Finished successfully.")
    print("=" * 80)


if __name__ == "__main__":
    main()