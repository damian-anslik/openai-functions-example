import os
import json
import dotenv
import openai
import functions

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
completion_model = os.getenv("OPENAI_COMPLETION_MODEL")


def get_chat_completion(messages: list[dict], available_functions: list[dict]) -> dict:
    response = openai.ChatCompletion.create(
        model=completion_model,
        messages=messages,
        functions=available_functions,
    )
    return response


def handle_function_call(messages: list[dict], available_functions: list[dict]) -> dict:
    completion_message = messages[-1]
    function_name = completion_message["function_call"]["name"]
    function_args = json.loads(completion_message["function_call"]["arguments"])
    function_call_result = None
    match function_name:
        # NOTE Register calls to functions here
        case "get_current_weather":
            function_call_result = functions.get_current_weather(**function_args)
        case _:
            raise NotImplementedError(f"Function {function_name} not implemented")
    if function_call_result is None:
        raise ValueError(f"Function {function_name} returned None")
    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": json.dumps(function_call_result),
        }
    )
    completion = get_chat_completion(
        messages=messages,
        available_functions=available_functions,
    )
    completion_details = completion["choices"][0]
    completion_message = completion_details["message"]
    return completion_message


def main(prompt: str):
    messages = [
        {"role": "user", "content": prompt},
    ]
    available_functions = functions.available_functions
    completion = get_chat_completion(
        messages=messages, available_functions=available_functions
    )
    completion_details = completion["choices"][0]
    finish_reason = completion_details["finish_reason"]
    completion_message = None
    match finish_reason:
        case "stop":
            completion_message = completion_details["message"]
        case "function_call":
            messages.append(completion_details["message"])
            completion_message = handle_function_call(
                messages=messages, available_functions=available_functions
            )
        case _:
            raise NotImplementedError(f"Finish reason {finish_reason} not implemented")
    print(completion_message["content"])


if __name__ == "__main__":
    main(prompt="What's the weather like in San Francisco?")
