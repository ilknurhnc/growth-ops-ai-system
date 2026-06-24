from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent
RAW_LEADS_PATH = BASE_DIR / "data" / "raw_leads.csv"


def check_required_files():
    if not RAW_LEADS_PATH.exists():
        raise FileNotFoundError(
            "data/raw_leads.csv bulunamadı. Önce lead datasını eklemelisin."
        )


def run_step(script_path):
    print(f"\nRunning: {script_path}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR
    )

    if result.returncode != 0:
        print(f"Step failed: {script_path}")
        sys.exit(1)


def main():
    print("Starting Growth Automation & AI Ops Pipeline...")

    check_required_files()

    run_step(BASE_DIR / "src" / "ai_ops_workflow.py")
    run_step(BASE_DIR / "src" / "outreach_sequence.py")
    run_step(BASE_DIR / "src" / "outreach_generator.py")

    print("\nPipeline completed successfully.")
    print("Generated files:")
    print("- data/ai_ops_output.csv")
    print("- data/outreach_sequence_output.csv")
    print("- data/outreach_messages.csv")


if __name__ == "__main__":
    main()