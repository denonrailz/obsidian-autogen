import gradio as gr
import os
import autogen
import multiprocessing as mp
from agent_init import initialize_agents

TIMEOUT = 60


def initiate_chat(problem, queue, n_results=3):
    assistant.reset()
    try:
        ragproxyagent.initiate_chat(
            assistant, problem=problem, silent=True, n_results=n_results
        )
        messages = ragproxyagent.chat_messages
        messages = [messages[k] for k in messages.keys()][0]
        messages = [m["content"] for m in messages if m["role"] == "user"]
    except Exception as e:
        messages = [str(e)]
    queue.put(messages)


def chatbot_reply(input_text):
    queue = mp.Queue()
    process = mp.Process(
        target=initiate_chat,
        args=(input_text, queue),
    )
    process.start()
    try:
        process.join(TIMEOUT+2)
        messages = queue.get(timeout=TIMEOUT)
    except Exception as e:
        messages = [
            str(e)
            if len(str(e)) > 0
            else "Invalid Request to OpenAI, please check your API keys."
        ]
    finally:
        try:
            process.terminate()
        except:
            pass
    return messages


with gr.Blocks() as demo:
    config_file_path = os.path.join(os.path.dirname(__file__), "OAI_CONFIG_LIST")
    config_list_file = autogen.config_list_from_json(
        env_or_file=config_file_path,
        filter_dict={
            "model": {
                "gpt-3.5-turbo",
                "gpt-4",
            },
        },
    )

    config_list_file[0]["model"] = "gpt-3.5-turbo"  # change model to gpt-35-turbo
 
    assistant, ragproxyagent = initialize_agents(config_list_file)

    conversations = {}
    autogen.ChatCompletion.start_logging(conversations)

    gr.Markdown("""
    # PAAS Chatbot Demo
    This demo shows how to use the PAAS Chatbot.
    """)
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "assets/assistant.png"))),
        # height=600,
    )

    txt_input = gr.Textbox(
        scale=4,
        show_label=False,
        placeholder="Enter text and press enter",
        container=False,
    )

    def respond(message, chat_history):

        messages = chatbot_reply(message)
        _msg = (
            messages[-1]
            if len(messages) > 0 and messages[-1] != "TERMINATE"
            else messages[-2]
            if len(messages) > 1
            else "Context is not enough for answering the question. Please press `enter` in the context url textbox to make sure the context is activated for the chat."
        )
        chat_history.append((message, _msg))

        # print("----- conversations -----")
        # print(conversations)

        return "", chat_history

    txt_input.submit(
        respond,
        [txt_input, chatbot],
        [txt_input, chatbot],
    )

if __name__ == "__main__":
    demo.launch(share=True)

