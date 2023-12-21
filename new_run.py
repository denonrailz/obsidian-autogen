from utils import (
    read_jsonl, create_timestamp_folder, get_response, collect_data_for_json_result, save_jsonl
)
from preferences.settings import results_folder, logs_folder, config_list

FAKE_ANSWERS = True
FAKE_EVALS = True


def main(fake_mode, config) -> None:
    question_list = read_jsonl()
    create_timestamp_folder(results_folder)
    create_timestamp_folder(logs_folder)
    results = get_response(fake_mode, config, question_list)
    json_results = collect_data_for_json_result(results)
    save_jsonl(json_results)


def eval():
    # придумать формат файла оценки
    # выдать фейковую оценку
    pass


if __name__ == "__main__":
    main(FAKE_ANSWERS, config_list)
    # print(read_jsonl()[0]['input'])
