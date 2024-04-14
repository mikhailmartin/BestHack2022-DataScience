import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_source_f(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_csv(
        input_data_path, usecols=["id_a", "source_f"], dtype={"source_f": "int8"}
    )

    features_from_source_f = (
        entire
        .groupby("id_a")
        .aggregate(
            #
            source_f_nunique=pd.NamedAgg(column="source_f", aggfunc="nunique"),
            #
            source_f_mean=pd.NamedAgg(column="source_f", aggfunc="mean"),
        )
    )

    features_from_source_f.to_csv(output_data_path)


if __name__ == "__main__":
    get_features_from_source_f()
