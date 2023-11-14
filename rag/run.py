import autogen
import agent_init
import os
import time
from datetime import datetime
from utils import save_logs, add_qa_item, create_md_file, create_logs_data


current_datetime = datetime.now()
instanceName = str(int(time.time())) + '.md'


config_list = autogen.config_list_from_json(
    env_or_file=os.path.join(os.path.dirname(__file__), "OAI_CONFIG_LIST"),
    filter_dict={
        "model": {
            "gpt-3.5-turbo",
            "gpt-4",
        },
    },
)

assistant, ragproxyagent = agent_init.initialize_agents(config_list)

settings_config = agent_init.parse_js_from_md(
    agent_init.obsdn_folder + agent_init.obsdn_settings_cfg
)
current_version = settings_config["agent_version"]

questions = agent_init.parse_md_files(
    os.path.join(agent_init.obsdn_folder, agent_init.obsdn_tests_folder)
)

qa_list = []

i = 0
print(f"\n\n>>>>>>>>>>>>  Below are outputs of Case {i+1}  <<<<<<<<<<<<\n\n")

assistant.reset()    
qa_problem = questions[i]['question']

autogen.ChatCompletion.start_logging(compact=True)
ragproxyagent.initiate_chat(
    assistant, problem=qa_problem, silent=True, n_results=5
)


for agent, messages in assistant.chat_messages.items():
    for message in messages:
        print(message['role'])
        print(message['content'])


summary = autogen.ChatCompletion.logged_history
autogen.ChatCompletion.stop_logging()

logs_data = create_logs_data(summary, current_datetime)
save_logs(logs_data, current_version)

add_qa_item(qa_problem, assistant.last_message()['content'])


if __name__ == "__main__":
    create_md_file(
        agent_init.obsdn_folder + agent_init.obsdn_results_folder + current_version,
        instanceName,
        qa_list
    )
