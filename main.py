import os
import json
import dotenv
import openai
import functions

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
available_functions = functions.available_functions
completion_model = os.getenv("OPENAI_COMPLETION_MODEL")


def send_completion_request(messages: list[dict]) -> dict:
    return openai.ChatCompletion.create(
        model=completion_model,
        messages=messages,
        functions=available_functions,
    )


def handle_function_call(messages: list[dict]) -> dict:
    """
    Extract the function name and arguments from the last message in the chat. Call the function and return the result.
    Pass the result to the completion model as a message. Return the completion message.
    """
    function_call_message = messages[-1]
    function_name = function_call_message["function_call"]["name"]
    function_args = json.loads(function_call_message["function_call"]["arguments"])
    function_call_result = functions.function_call(function_name, function_args)
    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": json.dumps(function_call_result),
        }
    )
    completion = send_completion_request(messages)
    completion_details = completion["choices"][0]
    completion_message = completion_details["message"]
    return completion_message


def generate_completion(prompt: str) -> dict:
    """
    Get a completion from the OpenAI API for the given prompt. If the completion is a function call, calls the function and return the result.
    """
    user_message = {"role": "user", "content": prompt}
    messages = [user_message]
    completion = send_completion_request(messages)
    completion_details = completion["choices"][0]
    finish_reason = completion_details["finish_reason"]
    completion_message = completion_details["message"]
    if finish_reason == "function_call":
        messages.append(completion_message)
        return handle_function_call(messages)
    return completion_message


if __name__ == "__main__":
    completion = generate_completion(prompt="What's the weather like in San Francisco?")
    print(completion)
