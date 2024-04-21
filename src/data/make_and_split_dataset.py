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

    targets = pd.read_csv(targets_path, dtype={"split": "category"})
    targets["target"] = (
        targets["target"]
        .replace({
            0.: "не спам",
            1.: "небольшие полезные ИП / малые бизнесы",
            2.: "организации",
            3.: "мобильная карусель",
            4.: "чёрные спаммеры и мошенники",
        })
        .astype("category")
    )

    for file_name in os.listdir(features_path):
        if not file_name.startswith("features_from_"):
            continue

        file_path = os.path.join(features_path, file_name)
        feature = pd.read_parquet(file_path)

        targets = targets.merge(feature, left_on="id", right_on="id_src", how="left")
        targets.drop(columns="id_src", inplace=True)

    train_data = targets.query("split == 'train'").drop(columns="split").dropna()
    train_data_path = os.path.join(output_data_path, "train_data.parquet")
    train_data.to_parquet(train_data_path, index=False)

    test_data = targets.query("split == 'test'").drop(columns=["split", "target"])
    test_data_path = os.path.join(output_data_path, "test_data.parquet")
    test_data.to_parquet(test_data_path, index=False)


if __name__ == "__main__":
    make_and_split_dataset()
