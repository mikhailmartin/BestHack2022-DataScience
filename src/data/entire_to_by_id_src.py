import os

import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True, file_okay=True))
@click.argument("targets_path", type=click.Path(exists=True, file_okay=True))
@click.argument("output_data_path", type=click.Path())
def entire_to_by_id_src(
        input_data_path: str, targets_path: str, output_data_path: str
) -> None:
    """Разбивает сырые звонки из единого файла на файлы по клиентам."""
    data = pd.read_parquet(input_data_path)

    targets = pd.read_csv(
        targets_path,
        usecols=["id", "split"],
        dtype={"split": "category"},
        index_col="id",
    )

    if not os.path.exists(os.path.join(output_data_path, "train")):
        os.makedirs(os.path.join(output_data_path, "train"))
    if not os.path.exists(os.path.join(output_data_path, "test")):
        os.makedirs(os.path.join(output_data_path, "test"))

    for id_src, data_by_id_src in data.groupby("id_src"):
        split = targets.loc[id_src, "split"]
        file_path = os.path.join(output_data_path, split, f"id_src={id_src}.parquet")
        data_by_id_src.to_parquet(file_path, index=False)


if __name__ == "__main__":
    entire_to_by_id_src()
