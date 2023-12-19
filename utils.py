import json
import os
import time


def read_jsonl() -> list:
    json_lines = []
    with open('tests/banking/samples2.jsonl', 'r') as file:
        for line in file:
            json_lines.append(json.loads(line))
    return json_lines


def create_timestamp_folder(path) -> None:
    if not os.path.exists(path):
        print('CREATE!!')
        os.makedirs(path)
