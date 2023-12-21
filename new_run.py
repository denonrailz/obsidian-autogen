from utils import (
    read_jsonl, create_timestamp_folder, get_response
)
from preferences.settings import results_folder, logs_folder, config_list

FAKE_ANSWERS = True
FAKE_EVALS = True


def main(fake_mode, config) -> None:
    question_list = read_jsonl()
    create_timestamp_folder(results_folder)
    create_timestamp_folder(logs_folder)
    get_response(fake_mode, config, question_list)
    # print(get_response(config, question_list))





def save_logs():
    # сохранить в json фейковый ответ
    pass


def eval():
    # придумать формат файла оценки
    # выдать фейковую оценку
    pass


if __name__ == "__main__":
    main(FAKE_ANSWERS, config_list)
    # print(read_jsonl()[0]['input'])
