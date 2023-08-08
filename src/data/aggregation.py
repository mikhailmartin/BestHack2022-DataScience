import click
import pandas as pd


@click.command()
@click.argument('input_data_path', type=click.Path(exists=True))
@click.argument('output_data_path', type=click.Path())
def main(input_data_path: str, output_data_path: str) -> None:

    entire = pd.read_csv(
        input_data_path,
        parse_dates=['datetime'],
        dtype={
            'time_zone': 'int8',
            'forward': 'int8',
            'zero_call_flg': 'int8',
            'source_b': 'int8',
            'source_f': 'int8',
            'num_b_length': 'int8',
            'duration': 'int16',
        },
    )

    aggregated = entire.groupby('id_a').aggregate(
        # количество уникальных адресатов
        dst_nunique=pd.NamedAgg(column='id_b', aggfunc='nunique'),

        # средний перерыв между звонками в секундах
        diff_mean=pd.NamedAgg(column='datetime', aggfunc=lambda s: s.diff()[1:].dt.seconds.mean()),
        # стандартное отклонение перерывов между звонками в секундах
        diff_std=pd.NamedAgg(column='datetime', aggfunc=lambda s: s.diff()[1:].dt.seconds.std()),

        # количество уникальных временных зон
        time_zone_nunique=pd.NamedAgg(column='time_zone', aggfunc='nunique'),

        # всего звонков
        calls_count=pd.NamedAgg(column='duration', aggfunc='count'),
        # средняя продолжительность звонка
        duration_mean=pd.NamedAgg(column='duration', aggfunc='mean'),
        # стандартное отклонение продолжительности звонка
        duration_std=pd.NamedAgg(column='duration', aggfunc='std'),

        #
        forward_nunique=pd.NamedAgg(column='forward', aggfunc='nunique'),
        #
        forward_mean=pd.NamedAgg(column='forward', aggfunc='mean'),

        #
        zero_call_flg_nunique=pd.NamedAgg(column='zero_call_flg', aggfunc='nunique'),
        #
        zero_call_flg_mean=pd.NamedAgg(column='zero_call_flg', aggfunc='mean'),

        #
        source_b_nunique=pd.NamedAgg(column='source_b', aggfunc='nunique'),
        #
        source_b_mean=pd.NamedAgg(column='source_b', aggfunc='mean'),

        #
        source_f_nunique=pd.NamedAgg(column='source_f', aggfunc='nunique'),
        #
        source_f_mean=pd.NamedAgg(column='source_f', aggfunc='mean'),

        #
        num_b_length_mean=pd.NamedAgg(column='num_b_length', aggfunc='mean'),
        #
        num_b_length_std=pd.NamedAgg(column='num_b_length', aggfunc='std'),
    )

    aggregated.to_csv(output_data_path)


if __name__ == '__main__':
    main()
