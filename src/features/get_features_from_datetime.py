import click
import pandas as pd


@click.command()
@click.argument(
    "input_data_path", type=click.Path(exists=True, file_okay=True)
)
@click.argument("output_data_path", type=click.Path(file_okay=True))
def get_features_from_datetime(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_parquet(input_data_path, columns=["id_src", "datetime"])

    features_from_datetime = (
        entire
        .groupby("id_src")
        .aggregate(
            # средний перерыв между звонками в секундах
            diff_mean=pd.NamedAgg(column="datetime", aggfunc=diff_mean),
            # стандартное отклонение перерывов между звонками в секундах
            diff_std=pd.NamedAgg(column="datetime", aggfunc=diff_std),
        )
        .reset_index()
    )

    features_from_datetime.to_parquet(output_data_path, index=False)


def diff_mean(series: pd.Series) -> pd.Series:
    return series.diff()[1:].dt.seconds.mean()


def diff_std(series: pd.Series) -> pd.Series:
    return series.diff()[1:].dt.seconds.std()


if __name__ == "__main__":
    get_features_from_datetime()
