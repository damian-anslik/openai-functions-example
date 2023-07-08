import os
import json
import dotenv
import openai
import functions

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
completion_model = os.getenv("OPENAI_COMPLETION_MODEL")


def get_chat_completion(messages: list[dict]) -> dict:
    response = openai.ChatCompletion.create(
        model=completion_model,
        messages=messages,
        functions=functions.available_functions,
    )
    return response


def handle_function_call(messages: list[dict]) -> dict:
    completion_message = messages[-1]
    function_name = completion_message["function_call"]["name"]
    function_args = json.loads(completion_message["function_call"]["arguments"])
    try:
        function_call_result = functions.function_call(function_name, function_args)
    except Exception as e:
        raise ValueError(f"Function call failed: {e}")
    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": json.dumps(function_call_result),
        }
    )
    completion = get_chat_completion(messages)
    completion_details = completion["choices"][0]
    completion_message = completion_details["message"]
    return completion_message


def main(prompt: str) -> dict:
    messages = [
        {"role": "user", "content": prompt},
    ]
    completion = get_chat_completion(messages)
    completion_details = completion["choices"][0]
    finish_reason = completion_details["finish_reason"]
    completion_message = None
    match finish_reason:
        case "stop":
            completion_message = completion_details["message"]
        case "function_call":
            messages.append(completion_details["message"])
            completion_message = handle_function_call(messages)
        case _:
            raise NotImplementedError(f"Finish reason {finish_reason} not implemented")
    return completion_message


if __name__ == "__main__":
    response = main(prompt="What's the weather like in San Francisco?")
    print(response)
