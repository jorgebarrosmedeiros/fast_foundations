"""Tests for the cleaning module"""
import pandas as pd
import argparse

from life_expectancy.cleaning import main
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
    #clean_data(region=args.region)
    #clean_data()
    parser = argparse.ArgumentParser(description="Clean life expectancy data.")
    parser.add_argument(
        "--region",
        default="PT",
        help="Region to filter the data (default is PT).",
    )
    args = parser.parse_args()
    main(
        file_path_to_read="eu_life_expectancy_raw.tsv",
        filename_to_save="pt_life_expectancy",
        path_to_save="/Users/jorge/Documents/Repos/faast-foundations/production/" \
                     "fast_foundations/life_expectancy/data",
        region=args.region,
    )
    
    pt_life_expectancy_actual = pd.read_csv(OUTPUT_DIR / "pt_life_expectancy.csv")
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
