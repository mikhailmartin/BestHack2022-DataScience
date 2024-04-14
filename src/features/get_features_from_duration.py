import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_duration(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_csv(
        input_data_path, usecols=["id_a", "duration"], dtype={"duration": "int16"}
    )

    features_from_duration = (
        entire
        .groupby("id_a")
        .aggregate(
            # всего звонков
            calls_count=pd.NamedAgg(column="duration", aggfunc="count"),
            # средняя продолжительность звонка
            duration_mean=pd.NamedAgg(column="duration", aggfunc="mean"),
            # стандартное отклонение продолжительности звонка
            duration_std=pd.NamedAgg(column="duration", aggfunc="std"),
        )
    )

    features_from_duration.to_csv(output_data_path)


if __name__ == "__main__":
    get_features_from_duration()
