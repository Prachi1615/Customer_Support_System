from openai import OpenAI

import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set your OpenAI API key

# Read product descriptions from a JSON file
with open('product_description.json', 'r') as file:
    product_descriptions = json.load(file)

# Ensure product_descriptions is a string
product_descriptions_str = json.dumps(product_descriptions)

# Generate a customer's comment using ChatGPT
def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature, 
    max_tokens=max_tokens)
    return response.choices[0].message.content

delimiter = "####"

############################################################
# System Message for 
# - User's Request about Products 
# - User's Request about Router
############################################################
system_message = f"""
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.

Output a python list of objects, where each object has \
the following format:

    'category': <one of Computers and Laptops, \
    Smartphones and Accessories, \
    Televisions and Home Theater Systems, \
    Gaming Consoles and Accessories, 
    Audio Equipment, Cameras and Camcorders>,

OR

    'products': <a list of products that must \
    be found in the allowed products below>

Where the categories and products must be found in \
the customer service query.

If a product is mentioned, it must be associated with \
the correct category in the allowed products list below.

If no products or categories are found, output an \
empty list.

Allowed products: 

Computers and Laptops category:
TechPro Ultrabook
BlueWave Gaming Laptop
PowerLite Convertible
TechPro Desktop
BlueWave Chromebook

Smartphones and Accessories category:
SmartX ProPhone
MobiTech PowerCase
SmartX MiniPhone
MobiTech Wireless Charger
SmartX EarBuds

Televisions and Home Theater Systems category:
CineView 4K TV
SoundMax Home Theater
CineView 8K TV
SoundMax Soundbar
CineView OLED TV

Gaming Consoles and Accessories category:
GameSphere X
ProGamer Controller
GameSphere Y
ProGamer Racing Wheel
GameSphere VR Headset

Audio Equipment category:
AudioPhonic Noise-Canceling Headphones
WaveSound Bluetooth Speaker
AudioPhonic True Wireless Earbuds
WaveSound Soundbar
AudioPhonic Turntable

Cameras and Camcorders category:
FotoSnap DSLR Camera
ActionCam 4K
FotoSnap Mirrorless Camera
ZoomMaster Camcorder
FotoSnap Instant Camera

Only output the list of objects, with nothing else.
""" # End of system_message

############################################################
# Test User Message 1: User's Request about Products
############################################################
user_message_1 = f"""
 tell me about the smartx pro phone and \
 the fotosnap camera, the dslr one. \
 Also tell me about your tvs """

messages =  [  
{'role':'system', 
 'content': system_message},    
{'role':'user', 
 'content': f"{delimiter}{user_message_1}{delimiter}"},  
] 

# - Rules:
# 1. If a product is mentioned in user_message, it must 
#    be associated with the correct category in the 
#    allowed products list above.
# 2. If no products or categories are found, output an \
#    empty list.
# - Both smartx pro phone
#   and fotosnap camera, the dslr one are found,
#   in the allowed products list
#   embedded in the system_message
category_and_product_response_1 = get_completion_from_messages(messages)
print(category_and_product_response_1)


# In[ ]:


############################################################
# Test User Message 2: User's Request about Router
############################################################
user_message_2 = f"""
my router isn't working"""

messages =  [  
{'role':'system',
 'content': system_message},    
{'role':'user',
 'content': f"{delimiter}{user_message_2}{delimiter}"},  
] 

# - Rules:
# 1. If a product is mentioned in user_message, it must 
#    be associated with the correct category in the 
#    allowed products list above.
# 2. If no products or categories are found, output an \
#    empty list.
# - No router is found in the allowed products list
#   embedded in the system_message
response = get_completion_from_messages(messages)
print(response)

def get_product_by_name(name):
    return product_descriptions.get(name, None)

############################################################
# Get the detailed information about all the products of a 
# category from detailed products information
############################################################
def get_products_by_category(category):
    return [product for product in product_descriptions.values() 
                  if product["category"] == category]


# In[ ]:


# Get Product by name from detailed products information
print(get_product_by_name("TechPro Ultrabook"))


# In[ ]:


# Get all the product of a category from 
# detailed products information
print(get_products_by_category("Computers and Laptops"))


# In[ ]:

# tell me about the smartx pro phone and \
# the fotosnap camera, the dslr one. \
# Also tell me about your tvs

print(user_message_1)


# In[ ]:

# Both smartx pro phone
# and fotosnap camera, the dslr one are found,
# in the allowed products list
# embedded in the system_message
print(category_and_product_response_1)


############################################################
# Step 2: Read Python string into Python list of dictionaries
############################################################

# In[ ]:

def read_string_to_list(input_string):
    if input_string is None:
        return None

    try:
        # Replace single quotes with double quotes for 
        # valid JSON
        input_string = input_string.replace("'", "\"")  
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None   
    


# In[ ]:


category_and_product_list = read_string_to_list(category_and_product_response_1)
print(category_and_product_list)


############################################################
# Step 3: Retrieve detailed product information for 
# the relevant products and categories
############################################################

# In[ ]:


def generate_output_string(data_list):
    output_string = ""

    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "products" in data:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4) + "\n"
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    output_string+= json.dumps(product, indent=4) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string 


# In[ ]:


product_information_for_user_message = generate_output_string(category_and_product_list)
print(product_information_for_user_message)


############################################################
# Step 4: Generate answer to user query based on 
#        detailed product information
#       
# - Make sure to ask the user relevant follow up questions.
############################################################

# In[ ]:


system_message = f"""
You are a customer service assistant for a \
large electronic store. \
Respond in a friendly and helpful tone, \
with very concise answers. \
Make sure to ask the user relevant follow up questions.
"""
user_message = f"""
tell me about the smartx pro phone and \
the fotosnap camera, the dslr one. \
Also tell me about your tvs"""

messages =  [  
{'role':'system',
 'content': system_message},   
{'role':'user',
 'content': user_message},  
{'role':'assistant',
 'content': f"""Relevant product information:\n\
 {product_information_for_user_message}"""},   
]

# Final response: 
#
# The SmartX ProPhone has a 6.1-inch display, 128GB storage, \
# 12MP dual camera, and 5G. The FotoSnap DSLR Camera \
# has a 24.2MP sensor, 1080p video, 3-inch LCD, and \
# interchangeable lenses. We have a variety of TVs, including \
# the CineView 4K TV with a 55-inch display, 4K resolution, \
# HDR, and smart TV features. We also have the SoundMax \
# Home Theater system with 5.1 channel, 1000W output, wireless \
# subwoofer, and Bluetooth. Do you have any specific questions \
# about these products or any other products we offer?
final_response = get_completion_from_messages(messages)
print(final_response)