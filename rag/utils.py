import os
import time

current_version = 0.1


def save_logs(data, version) -> None:
    """Writes logs from logs dict to rag/vaults/rag/logs/%version%/%timestamp."""
    timestamp = int(time.time())
    filename = str(timestamp) + '.md'
    path = 'vaults/rag/logs/' + str(version) + '/' + filename

    completion_tokens = data['completion_tokens']
    prompt_tokens = data['prompt_tokens']
    total_tokens = data['total_tokens']
    started_at = data['started_at']
    row_summary = data['row_summary']
    log_string = f'---\n' \
                 f'completion_tokens: {completion_tokens}\n' \
                 f'prompt_tokens: {prompt_tokens}\n' \
                 f'total_tokens: {total_tokens}\n' \
                 f'started_at: {started_at}\n' \
                 f'---\n' \
                 f'{row_summary}'

    with open(path, 'x') as file:
        file.write(log_string)


def create_logs_data(summary, current_datetime) -> dict:
    """Creates dict with logs data from summary from ChatCompletion.logged_history output."""
    summary_list = list(summary.values())

    return {
        'completion_tokens': summary_list[0]['token_count'][0]['completion_tokens'],
        'prompt_tokens': summary_list[0]['token_count'][0]['prompt_tokens'],
        'total_tokens': summary_list[0]['token_count'][0]['total_tokens'],
        'started_at': current_datetime.strftime("%d-%m-%YT%H:%M:%S"),
        'row_summary': summary
    }


def get_string_length(string, number):
    """Receive string and number and returns a string length of number."""
    return len(string) * number


def add_qa_item(question, history):
    print(history)
    # qa_list.append(QA(question, history[-1]['content']))


def create_md_file(path, filename, qa_list):
    if not os.path.exists(path):
        os.makedirs(path)

    filepath = os.path.join(path, filename)
    with open(filepath, "w") as f:
        f.write("---\n")
        f.write("started_at: " + str(int(time.time())) + "\n")
        f.write("type:\n")
        f.write("  - results\n")
        f.write("---\n")
        for qa in qa_list:
            f.write("##### Q: " + qa.question + "\n")
            f.write("A: " + qa.answer + "\n\n")


class QA:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
