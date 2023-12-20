import json
import os
import time

from autogen import OpenAIWrapper


def get_fake_response(question_list) -> list:
    question_count = 0
    results = []
    print('Start asking')
    for question in range(len(question_list)):
        question_count += 1
        result = [f'Fake answer for question {question_count}']
        print(f'Response for question {question_count} is {result}')
        results.append(results)
    print('End asking')
    return results


def get_autogen_response(config, question_list) -> list:
    client = OpenAIWrapper(config_list=config)
    question_count = 0
    results = []
    print('Start asking')
    for question in question_list:
        response = client.create(messages=question['input'])
        result = client.extract_text_or_completion_object(response)
        question_count += 1
        print(f'Response for question {question_count} is {result}')
        results.append(results)
    print('End asking')
    return results


def read_jsonl() -> list:
    json_lines = []
    path = 'tests/banking/samples3.jsonl'
    with open(path, 'r') as file:
        for line in file:
            json_lines.append(json.loads(line))
    questions = len(json_lines)
    # загрузить все файлы и все запросы
    # вывести в консоль сколько файлов загрузилось и вопросов в каждом.
    print(f'{questions} questions loaded from {path}.')
    return json_lines


def create_timestamp_folder(path) -> None:
    current_timestamp = str(int(time.time()))
    path += current_timestamp
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'Folder created in {path}.')


def get_response(fake_mode, config, question_list):
    if fake_mode:
        print('FAKE ANSWERS MODE!')
        get_fake_response(question_list)
    else:
        print('AUTOGEN ANSWERS MODE')
        get_autogen_response(config, question_list)


