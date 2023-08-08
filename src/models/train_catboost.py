import catboost
import click
import pandas as pd


RANDOM_STATE = 42


@click.command()
@click.argument('input_data_path', type=click.Path(exists=True))
@click.argument('output_model_path', type=click.Path())
def main(input_data_path: str, output_model_path: str) -> None:

    train_data = pd.read_csv(input_data_path, index_col='id_a')

    X_train = train_data.drop(columns='target')
    y_train = train_data['target'].replace({
        0.: 'не спам',
        1.: 'небольшие полезные ИП / малые бизнесы',
        2.: 'организации',
        3.: 'мобильная карусель',
        4.: 'чёрные спаммеры и мошенники',
    }).astype('category')

    model = catboost.CatBoostClassifier(verbose=False, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    model.save_model(output_model_path)


if __name__ == '__main__':
    main()
