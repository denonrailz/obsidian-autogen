import time
from utils import (
    read_jsonl_from_file, create_timestamp_folder, get_response,
    collect_data_for_json_result, save_jsonl_to_file, autogen_eval, collect_data_for_json_logs
)
from preferences.settings import (
    RESULTS_FOLDER, LOGS_FOLDER, config_list, RESULTS_FILE_NAME, EVALS_FILE_NAME, LOGS_FILE_NAME
)


def main(config) -> None:
    start_timestamp = str(int(time.time()))
    question_list = read_jsonl_from_file()
    create_timestamp_folder(RESULTS_FOLDER, start_timestamp)
    create_timestamp_folder(LOGS_FOLDER, start_timestamp)
    results = get_response(config, question_list)
    json_results = collect_data_for_json_result(results)
    json_logs = collect_data_for_json_logs(question_list)
    save_jsonl_to_file(json_results, start_timestamp, RESULTS_FOLDER, RESULTS_FILE_NAME)
    save_jsonl_to_file(json_logs, start_timestamp, LOGS_FOLDER, LOGS_FILE_NAME)
    json_evals = autogen_eval(json_results)
    save_jsonl_to_file(json_evals, start_timestamp, RESULTS_FOLDER, EVALS_FILE_NAME)


if __name__ == "__main__":
    main(config_list)
