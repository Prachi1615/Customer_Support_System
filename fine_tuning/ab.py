from openai import OpenAI
client = OpenAI()

completion = client.completions.create(
  model="model-name",
  prompt="Should I water the garden during a heatwave?",
  max_tokens=100
)
print(completion.choices[0].text)