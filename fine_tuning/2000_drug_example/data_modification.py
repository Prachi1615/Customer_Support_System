import json

conversations=[]
with open('drug_malady_data.jsonl', 'r') as f:
    for line in f:
        
        data = json.loads(line)
        
        prompt = data.get('prompt', '')
        completion = data.get('completion', '')
        
        conversation = {
            "messages": [
                {"role": "system", "content": ""},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": completion}
            ]
        }
        conversations.append(conversation)
        
with open('drug_malady_data1.jsonl', 'w') as new_file:
    for conversation in conversations:
        json.dump(conversation, new_file)
        new_file.write('\n')