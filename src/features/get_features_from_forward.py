import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def get_features_from_forward(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_csv(
        input_data_path, usecols=["id_a", "forward"], dtype={"forward": "int8"}
    )

    features_from_forward = (
        entire
        .groupby("id_a")
        .aggregate(
            #
            forward_nunique=pd.NamedAgg(column="forward", aggfunc="nunique"),
            #
            forward_mean=pd.NamedAgg(column="forward", aggfunc="mean"),
        )
    )

    features_from_forward.to_csv(output_data_path)


if __name__ == "__main__":
    get_features_from_forward()
