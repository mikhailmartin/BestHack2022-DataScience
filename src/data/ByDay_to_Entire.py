import os

import click
import pandas as pd


@click.command()
@click.argument("input_data_path", type=click.Path(exists=True))
@click.argument("output_data_path", type=click.Path())
def main(input_data_path: str, output_data_path: str) -> None:
    datas = []
    for file_name in os.listdir(input_data_path):
        file_path = os.path.join(input_data_path, file_name)
        data = pd.read_csv(
            file_path,
            dtype={
                "time_zone": "int8",
                "forward": "int8",
                "zero_call_flg": "int8",
                "source_b": "int8",
                "source_f": "int8",
                "num_b_length": "int8",
                "duration": "int16",
            },
        )
        datas.append(data)
    data = pd.concat(datas)

    data["datetime"] = pd.to_datetime(data["time_key"] + " " + data["start_time_local"])
    data = data.drop(columns=["time_key", "start_time_local"])

    data.to_csv(output_data_path, index=False)


if __name__ == "__main__":
    main()
