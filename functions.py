import random


def function_call(function_name: str, function_args: dict) -> dict:
    return globals()[function_name](**function_args)


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
