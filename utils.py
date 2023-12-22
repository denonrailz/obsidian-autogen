import json
import os
from random import random

from autogen import OpenAIWrapper
from preferences.settings import FAKE_ANSWERS, TEST_FOLDER


def get_fake_response(question_list) -> list:
    question_count = 0
    results = []
    print('Start asking')
    for question in question_list:
        question_count += 1
        answer = [f'Fake answer for question {question_count}']
        ideal = question['ideal']
        result = {'answer': answer, 'ideal': ideal}
        print(f'Response for question {question_count} is {result}')
        results.append(result)
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
        results.append(result)
    print('End asking')
    return results


def get_response(config, question_list):
    if FAKE_ANSWERS:
        print('FAKE ANSWERS MODE!')
        results = get_fake_response(question_list)
    else:
        print('AUTOGEN ANSWERS MODE')
        results = get_autogen_response(config, question_list)
    print('Results:', results)

    return results


def read_jsonl_from_file() -> list:
    json_lines = []
    path = f'tests/{TEST_FOLDER}/samples3.jsonl'
    with open(path, 'r') as file:
        for line in file:
            json_lines.append(json.loads(line))
    questions = len(json_lines)
    # загрузить все файлы и все запросы
    # вывести в консоль сколько файлов загрузилось и вопросов в каждом.
    print(f'{questions} questions loaded from {path}.')
    print(f'Questions: {json_lines}')
    return json_lines


def create_timestamp_folder(path, timestamp) -> None:
    path += timestamp
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'Folder created in {path}.')


def collect_data_for_json_result(results):
    line = 0
    json_results = []
    for result in results:
        json_line = {'line': line, 'result': result}
        json_results.append(json_line)
        line += 1
    print('JSON results list:', json_results)
    return json_results


def collect_data_for_json_logs(question_list):
    # сохранить в json фейковый ответ
    line = 0
    json_logs = []
    for question in question_list:
        system_prompt = question['input'][0]['content']
        user_prompt = question['input'][1]['content']
        json_line = {'system_prompt': system_prompt, 'user_prompt': user_prompt}
        json_logs.append(json_line)
        line += 1
    print('JSON logs list:', json_logs)
    return json_logs


def save_jsonl_to_file(items, start_timestamp, folder_name, file_name):
    path = f'{folder_name}{start_timestamp}/{file_name}.jsonl'
    with open(path, 'w') as outfile:
        for entry in items:
            json.dump(entry, outfile)
            outfile.write('\n')
    print(f'JSON {file_name} saved in {path}')


def autogen_eval(json_results):
    json_evals = []
    for result in json_results:
        line = result['line']
        eval_score = round(random(), 2)
        json_line = {'line': line, 'eval_score': eval_score}
        json_evals.append(json_line)
    print('JSON evals list:', json_evals)
    # придумать формат файла оценки
    # выдать фейковую оценку
    return json_evals
