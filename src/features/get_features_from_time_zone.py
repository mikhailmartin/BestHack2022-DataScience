import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_time_zone(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_parquet(input_data_path, columns=["id_src", "time_zone"])

    features_from_time_zone = (
        entire
        .groupby("id_src")
        # количество уникальных временных зон
        .aggregate(time_zone_nunique=pd.NamedAgg(column="time_zone", aggfunc="nunique"))
        .reset_index()
    )

    features_from_time_zone.to_parquet(output_data_path, index=False)


if __name__ == "__main__":
    get_features_from_time_zone()
