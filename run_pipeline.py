"""
Orchestrates the full healthcare pipeline end-to-end.
Runs each stage in order. If any stage fails, stops immediately (fail-fast).
"""
import sys

# Import the main function from each stage script
from setup_raw import setup_raw_layer
from load_raw import load_raw
from setup_staging import setup_staging_layer
from setup_rejected import setup_rejected
from load_staging_validated import load_staging_validated
from setup_marts import setup_marts_layer
from load_marts import load_marts
from setup_views import setup_views

def run_stage(name, func):
    """Run one stage, announce it, and fail-fast if it errors."""
    print(f"\n{'='*50}")
    print(f"▶  STAGE: {name}")
    print(f"{'='*50}")
    try:
        func()
    except Exception as e:
        print(f"❌ PIPELINE FAILED at stage '{name}': {e}")
        sys.exit(1)   # stop the whole pipeline — fail-fast

def main():
    print("🚀 STARTING HEALTHCARE PIPELINE")

    run_stage("1. Setup RAW",            setup_raw_layer)
    run_stage("2. Load RAW",             load_raw)
    run_stage("3. Setup STAGING",        setup_staging_layer)
    run_stage("4. Setup REJECTED",       setup_rejected)
    run_stage("5. Validate + Load",      load_staging_validated)
    run_stage("6. Setup MARTS",          setup_marts_layer)
    run_stage("7. Load MARTS",           load_marts)
    run_stage("8. Setup Views",          setup_views)

    print(f"\n{'='*50}")
    print("✅ PIPELINE COMPLETE — all stages succeeded")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()