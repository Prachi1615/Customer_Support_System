from openai import OpenAI
import os
from flask import Flask, render_template, request
from utility import get_completion
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from products_description import products_description


# read the api key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
sender_email = os.getenv("Email")
sender_password = os.getenv("Password")
recipient_email = os.getenv("Email2")


app = Flask(__name__, static_url_path='/static')


# Step 1: Generate Customer's Comment
def generate_customers_comment(products_description):
    prompt=f"""
    Assume that you are a customer to an electronic product company.
    Write a 100-word only comment about the products delimited by triple backticks in its own language. 
    Here's the plan.  We get the warhead, 
    and we hold the world ransom...
    ...FOR ONE MILLION DOLLARS!
    Products: ```{products_description}```
    """
    response=get_completion(prompt)
    return response

# Step 2: Generate Email Subject
def generate_email_subject(comment):
    prompt=f"""
    Asuming that you provide customer support for an electronic product company.
    Based on the customer comment delimited in triple backticks, suggest a short email subject to respond to customer. 
    Comment= ```{comment}```
    """
    response=get_completion(prompt)
    return response


# Step 3: Generate Customer Comment Summary
def summarized_comment(comment):
    prompt=f"""
    Asuming that you provide customer support for an electronic product company.
    Provide a concise summary in 50 words of the following customer comment delimited in triple backticks. Comment: ```{comment}```
    """
    response=get_completion(prompt)
    return response

def translate_summary(language, summary):
    prompt= f"""
    Translate the following summary delimited by triple backticks to the language delimited by <>. 
    Language:```{language}```   
    Summary:<{summary}>
    """
    response=get_completion(prompt)
    return response

# Step 4: Analyze Customer Comment Sentiment
def analyze_sentiment(comment):
    prompt=f"""
    Asuming that you provide customer support for an electronic product company.
    What is the sentiment of the comment delimited in triple backticks. Is it positive or negative? 
    Comment: ```{comment}```
    """
    max_tokens=10
    response=get_completion(prompt)
    sentiment = response.lower()
    if "positive" in sentiment:
        return "positive"
    elif "negative" in sentiment:
        return "negative"
    else:
        return "neutral"

# Step 5: Generate Email
def generate_customer_email(summary, sentiment, email_subject,language):
    if sentiment == "positive":
        response_text = "We're thrilled to hear your feedback and appreciate your positive words. Your satisfaction is our top priority!"
    elif sentiment == "negative":
        response_text = "We're truly sorry to hear about your experience. Your feedback is crucial, and we'll strive to address your concerns."
    else:
        response_text = "Thank you for your feedback! We're always looking to improve and your insights are valuable."
    prompt= f"""
    Asuming that you provide customer support for an electronic product company.
    Given the specified parameters below:
    - Comment summary enclosed in backticks (`{summary}`)
    - Our response text enclosed in triple quotes (\"\"\"{response_text}\"\"\")
    - Translate the Email subject enclosed in angle brackets ({email_subject}) to language \"{language}\"
    Write a complete email responding to the customer's comment using the language \"{language}\". 
    """
    response=get_completion(prompt)
    return response


@app.route('/', methods=['GET', 'POST'])

def index():
    answer = ""
    comment = generate_customers_comment(products_description)
    print("A customer comment has been generated.")
    if request.method == 'POST':
        language = request.form.get('language')  # Fetch language input from the webpage
        print(f"Selected language: {language}")
        answer = process_comment_to_email(comment, language)
    return render_template('index.html', question=comment, answer=answer)

def send_email(sender_email, sender_password, recipient_email, subject, body):
    # Create the MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Add body text to the email
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server (in this case, Gmail's SMTP server)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            # Start TLS for security'\
            server.ehlo()
            server.starttls()
            # Login to the email account
            server.login(sender_email, sender_password)
            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")








def process_comment_to_email(comment, language):
    email_subject = generate_email_subject(comment)
    print(f"Email's subject is generated as per the customer's comment")
    summary = summarized_comment(comment)
    print("Summary has been generated from the customer comment")
    translated_summary = translate_summary(language, summary)
    print(f"The summary has been translated to {language}")
    comment_sentiment = analyze_sentiment(comment)
    print(f"Sentiment of the comment: {comment_sentiment}")
    email_content = generate_customer_email(translated_summary, comment_sentiment, email_subject, language)
    print("Generated customer's email")
    send_email(sender_email, sender_password, recipient_email, email_subject, translated_summary)
    response = client.moderations.create(
    input="""
    Here's the plan.  We get the warhead, 
    and we hold the world ransom...
    ...FOR ONE MILLION DOLLARS!
    """
    )
    moderation_output = response.results[0]
    print(moderation_output)
    return email_content


if __name__ == '__main__':
    app.run(debug=True)