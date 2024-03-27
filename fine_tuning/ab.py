from openai import OpenAI
client = OpenAI()

completion = client.completions.create(
  model="ft:babbage-002:learninggpt:malady:96P7Bm2c",
  prompt="What is Botanica 3D Serum 30ml used for?",
  max_tokens=100
)
print(completion.choices[0].text)