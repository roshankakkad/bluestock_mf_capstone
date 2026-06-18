"""ETL pipeline entry point for the Bluestock Mutual Fund capstone.

This wrapper keeps the rubric-required filename (`etl_pipeline.py`) while
calling the master pipeline implementation in `run_pipeline.py`.
"""

from run_pipeline import main


if __name__ == "__main__":
    main()
