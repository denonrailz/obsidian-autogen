import autogen
import agent_init
import os
import chromadb
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import time

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
autogen.ChatCompletion.start_logging()

questions = agent_init.parse_md_files(os.path.join(agent_init.obsdn_folder, agent_init.obsdn_tests_folder))

test_results = []
class QA:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

qa_list = []

def add_qa_item(question, history):
    print(history)
    # qa_list.append(QA(question, history[-1]['content']))


# for i in range(len(questions)):
i = 0
print(f"\n\n>>>>>>>>>>>>  Below are outputs of Case {i+1}  <<<<<<<<<<<<\n\n")

assistant.reset()    
qa_problem = questions[i]['question']
ragproxyagent.initiate_chat(assistant, problem=qa_problem, silent=True, n_results=5)


# define functions that recives string and number and returns a string length of number
def get_string_length(string, number):
    return len(string) * number
        

for agent, messages in assistant.chat_messages.items():
    for message in messages:
        print(message['role'])
        print(message['content'])
    

print("keys: ", assistant.chat_messages.keys)
print("items: ", assistant.chat_messages.items)
print("values: ", assistant.chat_messages.values)
# add_qa_item(qa_problem, assistant.last_message()['content'])
add_qa_item(qa_problem, assistant.last_message()['content'])

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

create_md_file(agent_init.obsdn_folder+agent_init.obsdn_results_folder+current_version, instanceName, qa_list)