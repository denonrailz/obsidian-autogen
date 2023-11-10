import os
import time
from pathlib import Path

current_version = 0.1


def save_logs(version):
    BASE_DIR = str(Path(__file__).resolve().parent)

    timestamp = int(time.time())
    filename = str(timestamp) + '.md'
    path = 'vaults/rag/logs/' + str(version) + '/' + filename
    print(path)
    with open(path, 'x') as file:
        file.write('whatever')


def create_logs():
    pass


# define functions that recives string and number and returns a string length of number
def get_string_length(string, number):
    return len(string) * number


def add_qa_item(question, history):
    print(history)
    # qa_list.append(QA(question, history[-1]['content']))


def create_md_file(path, filename, qa_list):
    if not os.path.exists(path):
        os.makedirs(path)

    filepath = os.path.join(path, filename + ".md")
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
