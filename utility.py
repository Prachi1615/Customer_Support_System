import os
from openai import OpenAI
# read the api key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_completion(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content