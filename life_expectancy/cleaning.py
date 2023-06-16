"""
Assignment 2 - Life Expectanncy
"""

import os
import re
import argparse
from typing import Optional
from pandas import DataFrame
import pandas as pd


def clean_year(dataframe: DataFrame) -> DataFrame:
    """
    Cleans the year columns of the DataFrame by converting values to decimal numbers.

    Args:
        dataframe: DataFrame containing the data.

    Returns:
        DataFrame: DataFrame with the year columns cleaned and converted to decimal numbers.
    """
    dataframe["year"] = dataframe["year"].apply(
        lambda x: int(x.strip().replace(" ", ""))
    )

    dataframe["value"] = dataframe["value"].apply(extract_decimal_value)
    dataframe["value"] = pd.to_numeric(dataframe["value"], errors="coerce")

    return dataframe


def unpivot_table(dataframe: DataFrame) -> DataFrame:
    """
    Unpivots the table to a long format, creating the following
    columns: unit, sex, age, geo_time and values.

    Args:
        dataframe: DataFrame to be unpivoted.

    Returns:
        DataFrame: Unpivoted DataFrame.
    """
    unpivoted_df = dataframe.melt(
        id_vars=["unit,sex,age,geo\\time"], var_name="year", value_name="value"
    )
    unpivoted_table = unpivoted_df["unit,sex,age,geo\\time"].str.split(",", expand=True)
    unpivoted_table.columns = ["unit", "sex", "age", "region"]

    unpivoted_table_df = pd.concat([unpivoted_table, unpivoted_df], axis=1).drop(
        columns=["unit,sex,age,geo\\time"]
    )

    return unpivoted_table_df


def read_file(file_path: str, sep: str) -> DataFrame:
    """
    Reads a file into a DataFrame.

    Args:
        file_path: File path.
        sep: Separator used in the file.

    Returns:
        DataFrame: DataFrame containing the data from the file.
    """
    file_root_path = "life_expectancy/data"
    join_path = os.path.join(file_root_path, file_path)
    life_expectancy_raw = pd.read_csv(join_path, sep=sep)
    return life_expectancy_raw


def extract_decimal_value(string: Optional[str]) -> Optional[float]:
    """
    Extracts a decimal value from a string.

    Args:
        string: String to extract the decimal value from.

    Returns:
        Optional[float]: Decimal value extracted from the string.
    """
    if pd.notnull(string):
        pattern = r"(\d+(?:\.\d+)?)"
        decimal_values = re.findall(pattern, str(string))
        if decimal_values:
            return float(decimal_values[0])
    return None


def filter_region(dataframe: DataFrame, region: str) -> DataFrame:
    """
    Filters the DataFrame based on a specific region.

    Args:
        dataframe: DataFrame to be filtered.
        region: Region code to filter.

    Returns:
        DataFrame: Filtered DataFrame containing data only for the specified region.
    """
    dataframe = dataframe.loc[dataframe["region"] == region, :]
    return dataframe


def save_dataframe(dataframe: DataFrame, file_name: str, path: str) -> None:
    """
    Saves the DataFrame to a CSV file.

    Args:
        dataframe: DataFrame to be saved.
        file_name: Name of the file to save.
        path: Path where the file will be saved.

    Returns:
        None
    """
    path = "life_expectancy/data"
    dataframe.to_csv(
        os.path.join(path, f"{file_name}.csv"),
        index=False,
    )


def drop_null_values(dataframe: DataFrame, column: str) -> DataFrame:
    """
    Drops rows from a DataFrame where the specified column contains null values.

    Args:
        dataframe: DataFrame to be processed.
        column: Column name to check for null values.

    Returns:
        DataFrame: DataFrame with rows where the specified column does not contain null values.
    """
    dataframe = dataframe[~dataframe[column].isna()]
    return dataframe


def clean_data(
    file_path="eu_life_expectancy_raw.tsv",
    region="PT",
    path_to_save="life_expectancy/data",
    filename_to_save="pt_life_expectancy",
    dropna_column="value",
):
    """
    Cleans the data by reading the file, unpivoting the table,
    and cleaning the year columns, and filtering by region

    Args:
        file_path: File path.

    Returns:
        Saved dataframe
    """

    life_expec_df = read_file(file_path, sep="\t")

    life_expec_unpivot = unpivot_table(life_expec_df)

    life_expec_year_cleaned = clean_year(life_expec_unpivot)

    life_expec_no_null = drop_null_values(life_expec_year_cleaned, dropna_column)

    pt_life_expectancy = filter_region(life_expec_no_null, region)

    save_dataframe(
        pt_life_expectancy,
        filename_to_save,
        path_to_save,
    )

    return pt_life_expectancy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean life expectancy data.")
    parser.add_argument(
        "--region",
        default="PT",
        help="Region to filter the data (default is PT).",
    )
    args = parser.parse_args()
    clean_data(region=args.region)
