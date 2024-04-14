import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_time_zone(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_csv(
        input_data_path, usecols=["id_a", "time_zone"], dtype={"time_zone": "int8"}
    )

    features_from_time_zone = (
        entire
        .groupby("id_a")
        # количество уникальных временных зон
        .aggregate(time_zone_nunique=pd.NamedAgg(column="time_zone", aggfunc="nunique"))
    )

    features_from_time_zone.to_csv(output_data_path)


if __name__ == "__main__":
    get_features_from_time_zone()
