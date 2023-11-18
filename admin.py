from openai import OpenAI
import os
import time
import logging
import json
from utilities.ai_functions import *


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class Rogue:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.assistant = self.client.beta.assistants.retrieve("asst_320I6MdXAQVaoftlYKyOecPr")
        self.thread_id = 'thread_jumec4yKfkbUQGOaLYQ4DyK4'
        self.run = None

    def create_message_and_get_response(self, content):
        '''create the message by adding it to an existing thread'''
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=content
        )

        # create a run of that thread
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant.id
        )

        # Wait for the run to complete with exponential backoff and timeout
        run_status = run.status
        max_wait_time = 120  # Maximum wait time in seconds
        total_waited = 0
        wait_interval = 1  # Initial wait interval in seconds

        while run_status not in ["completed", "requires_action", "failed"]:
            if total_waited >= max_wait_time:
                logging.warning("Timeout reached while waiting for the run to complete.")
                return "Request timed out."

            time.sleep(wait_interval)
            total_waited += wait_interval
            wait_interval = min(wait_interval * 2, 10)  # Double the wait interval, up to 10 seconds

            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id
            )
            run_status = run.status

        # Check if run requires an action
        if run_status == "requires_action":
            required_actions = run.required_action.submit_tool_outputs.model_dump()
            logging.info("CALLLING REQUIRED ACIONS ======================== %s", required_actions["tool_calls"])
            tools_output = []
            for action in required_actions["tool_calls"]:
                func_name = action["function"]["name"]
                arguments = json.loads(action["function"]["arguments"])
                if func_name == "write_tweet":
                    tweet = ChiefTwit()
                    output = tweet.write_tweet(arguments["new_rate"])
                    tools_output.append({
                        "tool_call_id": action["id"],
                        "output": output
                    })
                else:
                    logging.info("+++++++++++++++++++++++ FUNCTION REQUIRED NOT FOUND! ++++++++++++++++++++++++")

            self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread_id,
                run_id=run.id,
                tool_outputs=tools_output,
            )
            time.sleep(2)
            run = self.client.beta.threads.runs.retrieve(
                        thread_id=self.thread_id,
                        run_id=run.id
                    )
            run_status = run.status
            # Exponential back off while waiting for run to complete or fail
            while run_status not in ["completed", "requires_action", "failed"]:
                if total_waited >= max_wait_time:
                    logging.warning("Timeout reached while waiting for the run to complete.")
                    return "Request timed out."
                else:
                    time.sleep(wait_interval)
                    total_waited += wait_interval
                    wait_interval = min(wait_interval * 2, 10)  # Double the wait interval, up to 10 seconds

                    run = self.client.beta.threads.runs.retrieve(
                        thread_id=self.thread_id,
                        run_id=run.id
                    )
                    run_status = run.status
            
            messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
            logging.info("+++++++++++++++++++++++ MESSAGES ++++++++++++++++++++++++ %s", messages.data)
            assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
            if assistant_messages:
                response = assistant_messages[0].content[0].text.value
                if response:
                    return response
                else:
                    return "Assistant response took time but action was carried out"
            else:
                return "No response from the assistant yet."
            
        else:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
            logging.info("+++++++++++++++++++++++ MESSAGES ++++++++++++++++++++++++ %s", messages.data)
            assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
            if assistant_messages:
                response = assistant_messages[0].content[0].text.value
                if response:
                    return response
                return 'My apologies boss, something went wrong while handling your request.\nPlease request again.'
            
class Kim:
    def __init__(self, thread_id):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.assistant = self.client.beta.assistants.retrieve("asst_P8iLGX94gzCwmRoB7HRQ7qNo")
        self.thread_id = thread_id
        self.run = None

    def create_message_and_get_response(self, content):
        '''create the message by adding it to an existing thread'''
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=content
        )

        # create a run of that thread
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant.id
        )

        # Wait for the run to complete with exponential backoff and timeout
        run_status = run.status
        max_wait_time = 120  # Maximum wait time in seconds
        total_waited = 0
        wait_interval = 1  # Initial wait interval in seconds

        while run_status not in ["completed", "requires_action", "failed"]:
            if total_waited >= max_wait_time:
                logging.warning("Timeout reached while waiting for the run to complete.")
                return "Request timed out."

            time.sleep(wait_interval)
            total_waited += wait_interval
            wait_interval = min(wait_interval * 2, 10)  # Double the wait interval, up to 10 seconds

            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id
            )
            run_status = run.status

        # Check if run requires an action
        if run_status == "requires_action":
            required_actions = run.required_action.submit_tool_outputs.model_dump()
            logging.info("CALLLING REQUIRED ACIONS ======================== %s", required_actions["tool_calls"])
            tools_output = []
            for action in required_actions["tool_calls"]:
                func_name = action["function"]["name"]
                arguments = json.loads(action["function"]["arguments"])
                if func_name == "set_rate":
                    output = set_rate(arguments["new_rate"])
                    tools_output.append({
                        "tool_call_id": action["id"],
                        "output": output
                    })
                else:
                    logging.info("+++++++++++++++++++++++ FUNCTION REQUIRED NOT FOUND! ++++++++++++++++++++++++")

            self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread_id,
                run_id=run.id,
                tool_outputs=tools_output,
            )
            time.sleep(2)
            run = self.client.beta.threads.runs.retrieve(
                        thread_id=self.thread_id,
                        run_id=run.id
                    )
            run_status = run.status
            # Exponential back off while waiting for run to complete or fail
            while run_status not in ["completed", "requires_action", "failed"]:
                if total_waited >= max_wait_time:
                    logging.warning("Timeout reached while waiting for the run to complete.")
                    return "Request timed out."
                else:
                    time.sleep(wait_interval)
                    total_waited += wait_interval
                    wait_interval = min(wait_interval * 2, 10)  # Double the wait interval, up to 10 seconds

                    run = self.client.beta.threads.runs.retrieve(
                        thread_id=self.thread_id,
                        run_id=run.id
                    )
                    run_status = run.status
            
            messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
            logging.info("+++++++++++++++++++++++ MESSAGES ++++++++++++++++++++++++ %s", messages.data)
            assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
            if assistant_messages:
                response = assistant_messages[0].content[0].text.value
                if response:
                    return response
                else:
                    return "Assistant response took time but action was carried out"
            else:
                return "No response from the assistant yet."
            
        else:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
            logging.info("+++++++++++++++++++++++ MESSAGES ++++++++++++++++++++++++ %s", messages.data)
            assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
            if assistant_messages:
                response = assistant_messages[0].content[0].text.value
                if response:
                    return response
                return 'My apologies boss, something went wrong while handling your request.\nPlease request again.'