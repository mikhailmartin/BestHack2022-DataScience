import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_num_b_length(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_csv(
        input_data_path,
        usecols=["id_a", "num_b_length"],
        dtype={"num_b_length": "int8"},
    )

    features_from_num_b_length = (
        entire
        .groupby("id_a")
        .aggregate(
            #
            num_b_length_mean=pd.NamedAgg(column="num_b_length", aggfunc="mean"),
            #
            num_b_length_std=pd.NamedAgg(column="num_b_length", aggfunc="std"),
        )
    )

    features_from_num_b_length.to_csv(output_data_path)


if __name__ == "__main__":
    get_features_from_num_b_length()
