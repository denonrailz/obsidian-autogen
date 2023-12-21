import json
import os
import time
# import jsonlines

from autogen import OpenAIWrapper


def get_fake_response(question_list) -> list:
    question_count = 0
    results = []
    print('Start asking')
    for question in range(len(question_list)):
        question_count += 1
        result = [f'Fake answer for question {question_count}']
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
        results = get_fake_response(question_list)
    else:
        print('AUTOGEN ANSWERS MODE')
        results = get_autogen_response(config, question_list)
    print('Results:', results)
    return results


def collect_data_for_json_result(results):
    line = 0
    json_results = []
    for result in results:
        json_line = {'line': line, 'answer': result}
        json_results.append(json_line)
        line += 1
    print('Json results:', json_results)
    return json_results


def save_logs(data):
    # сохранить в json фейковый ответ
    with open('results/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_jsonl(items):
    # with jsonlines.open('output.jsonl', 'w') as writer:
    #     writer.write_all(items)
    with open('results/data.jsonl', 'w') as outfile:
        for entry in items:
            json.dump(entry, outfile)
            outfile.write('\n')
