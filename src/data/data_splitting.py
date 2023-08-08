import os

import click
import pandas as pd


@click.command()
@click.argument('input_data_path', type=click.Path(exists=True))
@click.argument('targets_path', type=click.Path(exists=True))
@click.argument('output_data_path', type=click.Path())
def main(input_data_path: str, targets_path: str, output_data_path: str) -> None:

    data = pd.read_csv(input_data_path)
    targets = pd.read_csv(targets_path, dtype={'split': 'category', 'target': 'category'})

    data = data.merge(targets, left_on='id_a', right_on='id', how='left')
    data.drop(columns='id', inplace=True)  # дублирует d_a

    train_data = data.query('split == "train"')
    train_data.drop(columns='split', inplace=True)
    train_data.to_csv(os.path.join(output_data_path, 'train_data.csv'), index=False)

    test_data = data.query('split == "test"')
    test_data.drop(columns=['split', 'target'], inplace=True)
    test_data.to_csv(os.path.join(output_data_path, 'test_data.csv'), index=False)


if __name__ == '__main__':
    main()
