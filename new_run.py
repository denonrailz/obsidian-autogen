import os
import time
import autogen
from autogen import OpenAIWrapper

from utils import read_jsonl, create_timestamp_folder

current_timestamp = str(int(time.time()))
results_folder = 'results/' + current_timestamp


def main():
    # read_jsonl()
    create_timestamp_folder(results_folder)


config_list = autogen.config_list_from_json(
    env_or_file=os.path.join(os.path.dirname(__file__), "OAI_CONFIG_LIST"),
    filter_dict={
        "model": {
            "gpt-3.5-turbo",
            "gpt-4",
        },
    },
)

client = OpenAIWrapper(config_list=config_list)
response = client.create(messages=[{"role": "user", "content": "2+2="}])

print(client.extract_text_or_completion_object(response))


if __name__ == "__main__":
    main()
