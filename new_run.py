import os
import time
import autogen
from autogen import OpenAIWrapper

from utils import read_jsonl, create_timestamp_folder

current_timestamp = str(int(time.time()))
results_folder = 'results/' + current_timestamp
logs_folder = 'logs/' + current_timestamp

config_list = autogen.config_list_from_json(
    env_or_file=os.path.join(os.path.dirname(__file__), "OAI_CONFIG_LIST"),
    filter_dict={
        "model": {
            "gpt-3.5-turbo",
            "gpt-4",
        },
    },
)


def main(config):
    print(read_jsonl()[0]['input'])
    create_timestamp_folder(results_folder)
    create_timestamp_folder(logs_folder)
    client = OpenAIWrapper(config_list=config)
    response = client.create(messages=read_jsonl()[0]['input'])

    print(client.extract_text_or_completion_object(response))


def get_response():
    # обращаемся к автогену и получаем ответ
    response = 'response'
    return response


def save_logs():
    # сохранить в json фейковый ответ
    pass


def eval():
    # придумать формат файла оценки
    # выдать фейковую оценку
    pass


if __name__ == "__main__":
    main(config_list)
