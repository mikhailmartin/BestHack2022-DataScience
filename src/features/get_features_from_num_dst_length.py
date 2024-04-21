import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_num_dst_length(
        input_data_path: str, output_data_path: str
) -> None:

    entire = pd.read_parquet(input_data_path, columns=["id_src", "num_dst_length"])

    features_from_num_dst_length = (
        entire
        .groupby("id_src")
        .aggregate(
            #
            num_b_length_mean=pd.NamedAgg(column="num_dst_length", aggfunc="mean"),
            #
            num_b_length_std=pd.NamedAgg(column="num_dst_length", aggfunc="std"),
        )
        .reset_index()
    )

    features_from_num_dst_length.to_parquet(output_data_path, index=False)


if __name__ == "__main__":
    get_features_from_num_dst_length()
