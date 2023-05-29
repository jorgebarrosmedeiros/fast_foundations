"""Tests for the cleaning module"""
import pandas as pd
import argparse

from life_expectancy.cleaning import clean_data
from . import OUTPUT_DIR


def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
    parser = argparse.ArgumentParser(description="Clean life expectancy data.")
    parser.add_argument(
        "--region",
        default="PT",
        help="Region to filter the data (default is PT).",
    )
    args = parser.parse_args()
    clean_data(region=args.region)
    clean_data()
    pt_life_expectancy_actual = pd.read_csv(OUTPUT_DIR / "pt_life_expectancy.csv")
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
