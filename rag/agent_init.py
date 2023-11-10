import os
import re
import json
import chromadb
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import (
    RetrieveUserProxyAgent,
    PROMPT_CODE,
)

TIMEOUT = 600

obsdn_folder = "vaults/rag/"
obsdn_system_prompt = "prompts/assistant.md"
obsdn_agent_prompt = "prompts/proxy_agent.md"
obsdn_knowledge_folder = "Knowledges/"
obsdn_tests_folder = "tests/case02"
obsdn_retr_agent_cfg = "settings/retrieval_agent_config.md"
obsdn_settings_cfg = "settings/agent_settings.md"
obsdn_results_folder = "Results/"


def retrieve_file(path: str) -> str:
    with open(os.path.join(obsdn_folder, path), "r") as f:
        return f.read()


def parse_md_files(folder_path):
    results = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".md"):
            print(f"Parsing file: {file_name}")
            result = {}
            with open(os.path.join(folder_path, file_name), "r") as f:
                content = f.read()
                match = re.search(r"---\n(.*?)\n---\n(.*)", content, re.DOTALL)
                if match:
                    header = match.group(1)
                    body = match.group(2)
                    header = header.replace("\n  - ", ",")
                    for line in header.split("\n"):
                        if line.strip():
                            key_val = line.split(":", 1)
                            if len(key_val) == 2:
                                key, val = key_val
                                if key == "type":
                                    val = ",".join([v.strip() for v in val.split(",") if v.strip()])
                                result[key.strip()] = val.strip() if val.strip() else ""
                            else:
                                result[line.strip()] = ""
                    result["body"] = body.strip()
            results.append(result)
    return results


def parse_js_from_md(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    json_str = re.search('```javascript\n(.*)\n```', content, re.DOTALL).group(1)
    data = json.loads(json_str)
    return data


def initialize_agents(config_list):
    
    assistant_settings = parse_js_from_md(obsdn_folder+obsdn_settings_cfg)
    llm_config1 = {
        "request_timeout": assistant_settings["timeout"],
        "seed": assistant_settings["seed"],
        "config_list": config_list,
        "use_cache": assistant_settings["use_cache"],
        "temperature": assistant_settings["temperature"],
        "model": assistant_settings["model"]
    }

    assistant = RetrieveAssistantAgent(
        name="assistant",
        system_message=retrieve_file(obsdn_system_prompt),
        llm_config=llm_config1
    )

    retr_config = parse_js_from_md(obsdn_folder+obsdn_retr_agent_cfg)
    retr_config["client"] = chromadb.PersistentClient(path="/tmp/chromadb")
    retr_config["docs_path"] = obsdn_folder+obsdn_knowledge_folder
    retr_config["task"] = "qa"
    retr_config["customized_prompt"] = retrieve_file(obsdn_agent_prompt)

    ragproxyagent = RetrieveUserProxyAgent(
        name="ragproxyagent",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        retrieve_config=retr_config,
    )

    return assistant, ragproxyagent

