import autogen
import agent_init
import os
import time
from services import save_logs, get_string_length, add_qa_item, create_md_file

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

settings_config = agent_init.parse_js_from_md(agent_init.obsdn_folder+agent_init.obsdn_settings_cfg)
current_version = settings_config["agent_version"]

questions = agent_init.parse_md_files(
    os.path.join(agent_init.obsdn_folder, agent_init.obsdn_tests_folder)
)

test_results = []
qa_list = []


# for i in range(len(questions)):
i = 0
print(f"\n\n>>>>>>>>>>>>  Below are outputs of Case {i+1}  <<<<<<<<<<<<\n\n")

assistant.reset()    
qa_problem = questions[i]['question']

autogen.ChatCompletion.start_logging(compact=False)
ragproxyagent.initiate_chat(assistant, problem=qa_problem, silent=True, n_results=5)


for agent, messages in assistant.chat_messages.items():
    for message in messages:
        print(message['role'])
        print(message['content'])

print('!!!!!!!!!!!!!print_usage_summary!!!!!!!!!!')
autogen.ChatCompletion.print_usage_summary()
summary = autogen.ChatCompletion.logged_history
print(summary)
# summary_list = list(summary.values())
# print(summary_list)
# print(summary_list[0]['cost'])
# print(summary_list[0]['cost'])
# print(summary_list[0]['token_count'][0]['prompt_tokens'])
# print(summary_list[0]['token_count'][0]['total_tokens'])
# print(summary_list[0]['token_count'][0]['completion_tokens'])
autogen.ChatCompletion.stop_logging()

# print("keys: ", assistant.chat_messages.keys)
# print("items: ", assistant.chat_messages.items)
# print("values: ", assistant.chat_messages.values)
# add_qa_item(qa_problem, assistant.last_message()['content'])
add_qa_item(qa_problem, assistant.last_message()['content'])


if __name__ == "__main__":
    create_md_file(
        agent_init.obsdn_folder + agent_init.obsdn_results_folder + current_version,
        instanceName,
        qa_list
    )
