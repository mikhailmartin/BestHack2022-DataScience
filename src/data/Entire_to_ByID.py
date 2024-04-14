import os

import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True, file_okay=True))
@click.argument("targets_path", type=click.Path(exists=True, file_okay=True))
@click.argument("output_data_path", type=click.Path())
def main(input_data_path: str, targets_path: str, output_data_path: str) -> None:

    data = pd.read_csv(
        input_data_path,
        dtype={
            "time_zone": "int8",
            "forward": "int8",
            "zero_call_flg": "int8",
            "source_b": "int8",
            "source_f": "int8",
            "num_b_length": "int8",
            "duration": "int16",
        },
        parse_dates=["datetime"],
    )

    targets = pd.read_csv(
        targets_path,
        usecols=["id", "split"],
        dtype={"split": "category"},
        index_col="id",
    )

    if not os.path.exists(output_data_path):
        os.makedirs(os.path.join(output_data_path, "train"))
        os.makedirs(os.path.join(output_data_path, "test"))

    for id_a, data_by_id_a in data.groupby("id_a"):
        file_path = os.path.join(
            output_data_path, targets.loc[id_a, "split"], f"id_a={id_a}.csv"
        )
        data_by_id_a.to_csv(file_path, index=False)


if __name__ == "__main__":
    main()
