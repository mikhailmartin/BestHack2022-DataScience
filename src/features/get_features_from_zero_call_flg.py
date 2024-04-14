import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_zero_call_flg(
        input_data_path: str, output_data_path: str
) -> None:

    entire = pd.read_csv(
        input_data_path,
        usecols=["id_a", "zero_call_flg"],
        dtype={"zero_call_flg": "int8"},
    )

    features_from_zero_call_flg = (
        entire
        .groupby("id_a")
        .aggregate(
            #
            zero_call_flg_nunique=pd.NamedAgg(column="zero_call_flg", aggfunc="nunique"),
            #
            zero_call_flg_mean=pd.NamedAgg(column="zero_call_flg", aggfunc="mean"),
        )
    )

    features_from_zero_call_flg.to_csv(output_data_path)


if __name__ == "__main__":
    get_features_from_zero_call_flg()
