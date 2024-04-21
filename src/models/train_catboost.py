import catboost
import click
import pandas as pd


RANDOM_STATE = 42


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_model_path", type=click.Path())
def train_catboost(input_data_path: str, output_model_path: str) -> None:

    train_data = pd.read_parquet(input_data_path)

    X_train = train_data.drop(columns="target").set_index("id")
    y_train = train_data["target"]

    model = catboost.CatBoostClassifier(
        max_depth=5, verbose=False, random_state=RANDOM_STATE
    )
    model.fit(X_train, y_train)
    model.save_model(output_model_path)


if __name__ == "__main__":
    train_catboost()
