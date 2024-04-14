import click
import pandas as pd


@click.command()
@click.argument(
    "input_data_path", type=click.Path(exists=True, file_okay=True)
)
@click.argument("output_data_path", type=click.Path(file_okay=True))
def get_features_from_datetime(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_csv(
        input_data_path, usecols=["id_a", "datetime"], parse_dates=["datetime"]
    )

    features_from_datetime = (
        entire
        .groupby("id_a")
        .aggregate(
            # средний перерыв между звонками в секундах
            diff_mean=pd.NamedAgg(column="datetime", aggfunc=diff_mean),
            # стандартное отклонение перерывов между звонками в секундах
            diff_std=pd.NamedAgg(column="datetime", aggfunc=diff_std),
        )
    )

    features_from_datetime.to_csv(output_data_path)


def diff_mean(series: pd.Series) -> pd.Series:
    return series.diff()[1:].dt.seconds.mean()


def diff_std(series: pd.Series) -> pd.Series:
    return series.diff()[1:].dt.seconds.std()


if __name__ == "__main__":
    get_features_from_datetime()
