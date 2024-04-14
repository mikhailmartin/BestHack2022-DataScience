import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_id_b(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_csv(input_data_path, usecols=["id_a", "id_b"])

    features_from_id_b = (
        entire
        .groupby("id_a")
        # количество уникальных адресатов
        .aggregate(dst_nunique=pd.NamedAgg(column="id_b", aggfunc="nunique"))
    )

    features_from_id_b.to_csv(output_data_path)


if __name__ == "__main__":
    get_features_from_id_b()
