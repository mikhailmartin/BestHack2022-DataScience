import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_id_dst(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_parquet(input_data_path, columns=["id_src", "id_dst"])

    features_from_id_dst = (
        entire
        .groupby("id_src")
        # количество уникальных адресатов
        .aggregate(dst_nunique=pd.NamedAgg(column="id_dst", aggfunc="nunique"))
        .reset_index()
    )

    features_from_id_dst.to_parquet(output_data_path, index=False)


if __name__ == "__main__":
    get_features_from_id_dst()
