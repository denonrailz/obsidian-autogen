import json
import os
import time


def read_jsonl() -> list:
    json_lines = []
    with open('tests/banking/samples.jsonl', 'r') as file:
        for line in file:
            json_lines.append(json.loads(line))
            print(json_lines)
    return json_lines


def create_timestamp_folder(path):
    if not os.path.exists(path):
        print('CREATE!!')
        os.makedirs(path)
