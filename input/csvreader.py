"""Tool for reading the CSV room plan for the Bad Boll Seminaris."""


import os
from pathlib import Path

import pandas as pd


def extract_floor_plan(
    path_to_csv: Path | os.PathLike | str | bytes = None,
) -> pd.DataFrame:
    """Parse the CSV file containing relevant rooms and dimensions and
    return it as a `pandas.DataFrame`.

    Args:
        path_to_csv (Path | os.PathLike | str | bytes, optional): Pointer to the CSV file or stream. Defaults to None.

    Returns:
        pd.DataFrame: Content of the CSV file as dataframe.
    """
    if not path_to_csv:
        path_to_csv = Path.cwd() / "data/relevant_rooms.csv"
    df = pd.read_csv(
        filepath_or_buffer=path_to_csv,
    )
    return df


if __name__ == "__main__":
    print(extract_floor_plan())

