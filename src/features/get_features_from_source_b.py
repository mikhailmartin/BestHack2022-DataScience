import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_source_b(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_parquet(input_data_path, columns=["id_src", "source_b"])

    features_from_source_b = (
        entire
        .groupby("id_src")
        .aggregate(
            #
            source_b_nunique=pd.NamedAgg(column="source_b", aggfunc="nunique"),
            #
            source_b_mean=pd.NamedAgg(column="source_b", aggfunc="mean"),
        )
        .reset_index()
    )

    features_from_source_b.to_parquet(output_data_path, index=False)


if __name__ == "__main__":
    get_features_from_source_b()
