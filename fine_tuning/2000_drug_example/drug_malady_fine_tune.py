from openai import OpenAI
client = OpenAI()

# completion = client.chat.completions.create(
#   model="ft:gpt-3.5-turbo-0125:learninggpt:prachi:97wVRMB2",
#   messages=[{"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "What is Addnok Tablet 20'S used for?"}]
# )
# print(completion.choices[0].message.content)
drugs = [

"A CN Gel(Topical) 20gmA CN Soap 75gm", # Class 0

"Addnok Tablet 20'S", # Class 1

"ABICET M Tablet 10's", # Class 2

]

# Returns a drug class for each drug

for drug_name in drugs:

    prompt = [{"role": "system", "content": ""},
    {"role": "user", "content": "Drug: {}\nMalady:".format(drug_name)}]
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:learninggpt:prachi:97wVRMB2",
        messages= prompt
        )


    drug_class = response.choices[0].message.content
    print(drug_class)


drugs = [
    "What is 'A CN Gel(Topical) 20gmA CN Soap 75gm' used for?",  # Class 0
    "What is 'Addnok Tablet 20'S used for?",  # Class 1
    "What is 'ABICET M Tablet 10's used for?",  # Class 2
]

class_map = {
0: "Acne",
5: "Adhd",
2: "Allergies",
}


# Returns a drug class for each drug

for drug_name in drugs:

    prompt = [{"role": "system", "content": ""},
    {"role": "user", "content": "Drug: {}\nMalady:".format(drug_name)}]

    response = client.chat.completions.create(model="ft:gpt-3.5-turbo-0125:learninggpt:prachi:97wVRMB2",
                                         messages= prompt,
                                         temperature=1)

    res = response.choices[0].message.content

    try:

        print("\n",drug_name + " is used for " + class_map[int(res)])
        print()

    except:

        print("I don't know what " + drug_name + " is used for.")
