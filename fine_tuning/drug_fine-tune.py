from openai import OpenAI
client = OpenAI()

completion = client.completions.create(
  model="ft:davinci-002:learninggpt:drugmalady:97RgLZOR",
  prompt="What is A CN Gel(Topical) 20gmA CN Soap 75gm used for?",
  max_tokens=10
)
print(completion.choices[0].text)
drugs = [

"A CN Gel(Topical) 20gmA CN Soap 75gm", # Class 0

"Addnok Tablet 20'S", # Class 1

"ABICET M Tablet 10's", # Class 2

]

# Returns a drug class for each drug

for drug_name in drugs:

    prompt = "Drug: {}\nMalady:".format(drug_name)
    response = client.completions.create(
        model="ft:davinci-002:learninggpt:drugmalady:97RgLZOR",
        prompt= prompt,
        temperature=1,
        max_tokens=2,
        )


    drug_class = response.choices[0].text
    print(drug_class)


drugs = [
    "What is 'A CN Gel(Topical) 20gmA CN Soap 75gm' used for?",  # Class 0
    "What is 'Addnok Tablet 20'S' used for?",  # Class 1
    "What is 'ABICET M Tablet 10's' used for?",  # Class 2
]

class_map = {
0: "Acne",
1: "Adhd",
2: "Allergies",
}


# Returns a drug class for each drug

for drug_name in drugs:

    prompt = "Drug: {}\nMalady:".format(drug_name)

    response = client.completions.create(model="ft:davinci-002:learninggpt:drugmalady:97RgLZOR",
                                         prompt= prompt,
                                         temperature=1,
                                         max_tokens=1)

    response = response.choices[0].text

    try:

        print(drug_name + " is used for " + class_map[int(response)])

    except:

        print("I don't know what " + drug_name + " is used for.")
