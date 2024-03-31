
# Use Pandas to transform the data into the desired format.
import pandas as pd

######################################################################
# Read the first n rows from the Excel file
# - The number of rows to read from the Excel file, 
#   Medicine_description.xlsx, to 2000. 
#   + This means that we are going to use a dataset of 2000 drug 
#     names to fine-tune the model. 
# - You can use more.
######################################################################
n = 2000

df = pd.read_excel('Medicine_description.xlsx', sheet_name='Sheet1', 
        header=0, nrows=n)

# Get the unique values in the ‘Reason’ column of the data frame, 
# stores them in an array called reasons
reasons = df["Reason"].unique()

# Assigns a numerical index to each unique value in the reasons 
# array, and stores it in a dictionary called reasons_dict.
reasons_dict = {reason: i for i, reason in enumerate(reasons)}

# Add a new line and “Malady:” to the end of each drug name in 
# the ‘Drug_Name’ column of the data frame. 
# - The desired format:
#       Drug: <Drug_Name>\nMalady:

df["Drug_Name"] = "Drug: " + df["Drug_Name"] + "\n" + "Malady:"

# It concatenates a space and the corresponding numerical index 
# from the reasons_dict to the end of each 'Reason’ 
# value in the data frame.
df["Reason"] = " " + df["Reason"].apply(lambda x: "" + str(reasons_dict[x]))

# For this example, we don’t need the ‘Description’ column, that’s 
# why the script drops it from the data frame.
df.drop(["Description"], axis=1, inplace=True)

# Renaming the ‘Drug_Name’ column to ‘prompt’ 
# and the ‘Reason’ column to ‘completion’.
df.rename(columns={"Drug_Name": "prompt", "Reason": "completion"}, inplace=True)

# Convert the dataframe to jsonl format
jsonl = df.to_json(orient="records", indent=0, lines=True)

with open("drug_malady_data1.jsonl", "w") as f:
    f.write(jsonl)
