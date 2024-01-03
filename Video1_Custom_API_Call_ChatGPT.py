import json
import requests
from openai import OpenAI
OPENAI_API_KEY = "sk-XXXXXX" # replace your key
GPT_MODEL = "gpt-3.5-turbo-0613"
client = OpenAI(api_key=OPENAI_API_KEY)
# In production, this could be your backend API or an external API
messages = [{"role": "user", "content": "What's the weather like Hyderabad today"}]
custom_function = [
{
    "type": "function",
    "function": {
        "name": "get_weather_info",
        "description": "Get the current weather in a given location if weather not found anywhere take it from the accuweather.com",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "source":{
                    "type":"string",
                    "description":"Actual Source from where this weather has been pulled\
                        from example Weather Report Organisation name"
                    },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                "temperature": {"type": "string",
                                "description":"this should be the actual \
                                    weather example the temperature is 25 degrees"},
            },
            "required": ["location","source","unit","temperature"],
        },
    },
}]
response = client.chat.completions.create(
    model=GPT_MODEL,
    messages=messages,
    tools=custom_function
)
response_message = response.choices[0].message
tool_calls = response_message.tool_calls
#print(response_message)
arguments_dict = json.loads(response_message.tool_calls[0].function.arguments)
print(json.dumps(arguments_dict, indent=4))
