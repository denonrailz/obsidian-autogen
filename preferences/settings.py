import autogen
import os

FAKE_ANSWERS = True
FAKE_EVALS = True

TEST_FOLDER = 'banking'

RESULTS_FOLDER = 'results/'
LOGS_FOLDER = 'logs/'
RESULTS_FILE_NAME = 'results'
EVALS_FILE_NAME = 'evals'
LOGS_FILE_NAME = 'logs'

config_list = autogen.config_list_from_json(
    env_or_file=os.path.join(os.path.dirname(__file__), "OAI_CONFIG_LIST"),
    filter_dict={
        "model": {
            "gpt-3.5-turbo",
            "gpt-4",
        },
    },
)
