import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_source_b(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_csv(
        input_data_path, usecols=["id_a", "source_b"], dtype={"source_b": "int8"}
    )

    features_from_source_b = (
        entire
        .groupby("id_a")
        .aggregate(
            #
            source_b_nunique=pd.NamedAgg(column="source_b", aggfunc="nunique"),
            #
            source_b_mean=pd.NamedAgg(column="source_b", aggfunc="mean"),
        )
    )

    features_from_source_b.to_csv(output_data_path)


if __name__ == "__main__":
    get_features_from_source_b()
