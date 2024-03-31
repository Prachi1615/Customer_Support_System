import random
from sklearn.model_selection import train_test_split

import json

def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        for item in data:
            json.dump(item, file)  
            file.write('\n')

import json

def load_data_from_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            item = json.loads(line.strip())
            data.append(item)
    return data

data = load_data_from_file('drug_malady_data1.jsonl')


random.shuffle(data)

# Split the data into training and validation sets (80% training, 20% validation)
train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

save_data_to_file(train_data, 'drug_malady_train_data.jsonl')
save_data_to_file(val_data, 'drug_malady_val_data.jsonl')
