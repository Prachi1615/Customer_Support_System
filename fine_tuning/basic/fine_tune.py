from openai import OpenAI
client = OpenAI()

file=client.files.create(
  file=open("data_prepared.jsonl", "rb"),
  purpose="fine-tune"
)

model=client.fine_tuning.jobs.create(
  training_file=file.id,
  model="babbage-002"
)
print(model)