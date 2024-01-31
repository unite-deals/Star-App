import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai
import csv
import streamlit as st
import ssl
import yagmail

#from yagmail import Connect 
default_message = """
Hi |*FNAME*|,

I saw you are a growing company (Write more about this company so they can feel similarity). 

There are a lot of problems faced by companies like |*COMPANY*| (Search their industry and Niche to find out if they lack in Marketing and if they are tech phobic or not. If not then don't include this section)

The best part is... I have found the way to fix these

Just hit the Reply and I'll send you over a PDF explaining everything you need to know. OR JUST GIVE ME 15 MIN OF YOUR TIME AND I WILL BE THERE TO FIX YOUR PROBLEMS at https://calendly.com/zcops

Make sure have it fixed before your competitors get an edge on you

Best,
CeO
Star cement

P.S Don't wait for other to see if they get results. Start now and Start Early!!! 🚀✨
"""
default_author = "Rishi"
default_subject = "you might wanna have a look at this"

def personalize_email(email_template, first_name, last_name, company):
    """Personalizes the email text with various placeholders."""

    personalized_email = email_template.replace("|*FNAME*|", first_name)
    personalized_email = personalized_email.replace("|*LNAME*|", last_name)
    personalized_email = personalized_email.replace("|*COMPANY*|", company)
    personalized_email = personalized_email.replace("|*FULLNAME*|", f"{first_name} {last_name}")

    return personalized_email


def send_email(recipient, subject, body, attachment_path=None):
    # Set up your email credentials here
    #yag= Connect('creativeauthoronline@gmail.com' : 'Star Creative) 
    yag = yagmail.SMTP({'creativeauthoronline@gmail.com' : 'Star cement creative'}, 'dtil cwls dcai mogx')

    # Compose the email
    contents = [body]
    if attachment_path:
        contents.append(attachment_path)

    # Send the email
    yag.send(to=recipient, subject=subject, contents=contents)



genai.configure(api_key="AIzaSyDVQubOFyqyRDepOELUXwVRBMnbngkHYm8")

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config={
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    },
    safety_settings=[
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ],
)

def read_csv(file_object):
    csv_reader = csv.DictReader(file_object)
    return list(csv_reader)

def extract_data(csv_data):
    extracted_data = []

    for row in csv_data:
        first_name = row.get('First Name', '')
        last_name = row.get('Last Name', '')
        company = row.get('Company', '')
        email = row.get('Email', '')

        extracted_data.append({
            'First Name': first_name,
            'Last Name': last_name,
            'Company': company,
            'Email': email,
        })

    return extracted_data

def craft_message(csv_file,message=None,subject=None, author=None):
    data = read_csv(csv_file)
    extracted_data = extract_data(data)
    if subject is None:
        subject = default_subject
    if message is None:
        message = default_message
    if author is None:
        author = default_author
    for contact in extracted_data:
        first_name = contact["First Name"]
        last_name = contact["Last Name"]
        company = contact["Company"]
        email = contact["Email"]

        response =  model.generate_content([
                        f"Write an professional email within150 words  to {first_name} {last_name}\n\n"
                        f"search about this {company} so that you can make the message more personalized. "
                        f"The Niche of this company is {niche} You have to change the message such that it reflects "
                        f"the value of this company. Make sure to copy {autors} Style of Copywriting\n\n"
                        f"This is the Message:\n{message}\n\nThank you\n\n\nNOTE:Don't change the variables like "
                        f"|*FNAME*| or anything similar.\n\nDon't write any welcome messages like "
                        f"'I hope this message finds you well' because it looks usual. I want something unique\n\n"
                        f"Only Send the Email and don NOT include your text like 'Here is the Email'"
                        f"Warm Regards ,\n\n mention the senders name (Mr . Tapas ) and positions (CEO) from {niche} "
                    ])
 
        st.write(f"Email sent to {first_name} {last_name}")
        personalized_email = personalize_email(response.text, first_name, last_name, company)
        send_email(email, subject, personalized_email ,attachment_path)