import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_forward(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_parquet(input_data_path, columns=["id_src", "forward"])

    features_from_forward = (
        entire
        .groupby("id_src")
        .aggregate(
            #
            forward_nunique=pd.NamedAgg(column="forward", aggfunc="nunique"),
            #
            forward_mean=pd.NamedAgg(column="forward", aggfunc="mean"),
        )
        .reset_index()
    )

    features_from_forward.to_parquet(output_data_path, index=False)


if __name__ == "__main__":
    get_features_from_forward()
