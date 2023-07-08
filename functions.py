import random

available_functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
            },
            "required": ["location"],
        },
    }
]


def function_call(function_name: str, function_args: dict) -> dict:
    match function_name:
        case "get_current_weather":
            return get_current_weather(**function_args)
        case _:
            raise NotImplementedError(f"Function {function_name} not implemented")


def get_current_weather(location: str) -> dict:
    return {
        "temperature": random.randint(0, 35),
        "unit": "celsius",
        "description": random.choice(
            [
                "sunny",
                "cloudy",
                "rainy",
            ]
        ),
    }
