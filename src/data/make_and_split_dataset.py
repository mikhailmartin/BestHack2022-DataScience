import os

import click
import pandas as pd


@click.command()
@click.argument("targets_path", type=click.Path(exists=True))
@click.argument("features_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def make_and_split_dataset(
        targets_path: str, features_path: str, output_data_path: str
) -> None:

    targets = pd.read_csv(
        targets_path, dtype={"split": "category", "target": "category"}
    )

    for file_name in os.listdir(features_path):
        if not file_name.startswith("features_from_"):
            continue

        file_path = os.path.join(features_path, file_name)
        feature = pd.read_csv(file_path)

        targets = targets.merge(feature, how="left", left_on="id", right_on="id_a")
        targets.drop(columns="id_a", inplace=True)

    train_data = targets.query("split == 'train'")
    train_data.drop(columns="split", inplace=True)
    train_data.to_csv(os.path.join(output_data_path, "train_data.csv"), index=False)

    test_data = targets.query("split == 'test'")
    test_data.drop(columns=["split", "target"], inplace=True)
    test_data.to_csv(os.path.join(output_data_path, "test_data.csv"), index=False)


if __name__ == "__main__":
    make_and_split_dataset()
