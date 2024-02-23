#######################################################
# # L2: Evaluate Inputs: Classification
#######################################################
# ## Setup
# #### Load the API key and relevant Python libaries.
# In this course, we've provided some code that loads 
# the OpenAI API key for you.


#######################################################
# Classify customer queries to handle different cases
#
# - For tasks in which lots of independent sets 
#   of instructions are needed to handle different 
#   cases, it can be beneficial to 
#   1. first classify the type of query, and then 
#   2. use that classification to determine which 
#      instructions to use.
# - This can be achieved by defining 
#      1. fixed categories and 
#      2. hard-coding instructions 
#   that are relevant for handling tasks in a 
#   given category.
#######################################################

import os
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_completion_from_messages(messages, 
                 model="gpt-3.5-turbo", 
                 temperature=0, 
                 max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


# In[ ]:


delimiter = "####"

# System message 
system_message = f"""
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Classify each query into a primary category \
and a secondary category. 
Provide your output in json format with the \
keys: primary and secondary.

Primary categories: Billing, Technical Support, \
Account Management, or General Inquiry.

Billing secondary categories:
Unsubscribe or upgrade
Add a payment method
Explanation for charge
Dispute a charge

Technical Support secondary categories:
General troubleshooting
Device compatibility
Software updates

Account Management secondary categories:
Password reset
Update personal information
Close account
Account security

General Inquiry secondary categories:
Product information
Pricing
Feedback
Speak to a human

"""


#######################################################
# 1. Try the first user message
#    Account Management secondary categories
####################################################### 
# User message 
user_message = f"""\
I want you to delete my profile and all of my user data"""

# Combined messages to be sent to ChatGPT 
messages =  [  
{'role':'system', 
 'content': system_message},    
{'role':'user', 
 'content': f"{delimiter}{user_message}{delimiter}"},  
] 

# Get response from ChatGPT 
response = get_completion_from_messages(messages)
print(response)

# In[ ]:

#######################################################
# 2. Try the second user message
#    General Inquiry secondary categories
####################################################### 
user_message = f"""\
Tell me more about your flat screen tvs"""


# Combined messages to be sent to ChatGPT 
messages =  [  
{'role':'system', 
 'content': system_message},    
{'role':'user', 
 'content': f"{delimiter}{user_message}{delimiter}"},  
] 

# Get response from ChatGPT 
response = get_completion_from_messages(messages)
print(response)

# In[ ]:
    