import streamlit as st
import pandas as pd
#import openai
from pathlib import Path
import yagmail
import google.generativeai as genai
# Set your OpenAI API key here
#openai.api_key = 'your_openai_api_key'
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

def send_email(recipient, subject, body, attachment_path=None):
    # Set up your email credentials here
    yag = yagmail.SMTP('creativeauthoronline@gmail.com', 'dtil cwls dcai mogx')

    # Compose the email
    contents = [body]
    if attachment_path:
        contents.append(attachment_path)

    # Send the email
    yag.send(to=recipient, subject=subject, contents=contents)

def main():
    st.title("Email Sender with Streamlit")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded CSV file:")
        st.write(df)

        # Email details
        recipient = st.text_input("Recipient email:")
        subject = st.text_input("Email subject:")

        # Generate email body using GPT-3
        prompt = st.text_area("Prompt for email body generation:", "Dear [Recipient],\n\n")
        generated_body = model.generate_content(prompt)
        body = st.text_area("Generated Email body:", value=generated_body)

        # Attachments
        attachment_type = st.radio("Select attachment type", ["None", "Image", "PDF"])
        attachment_path = None

        if attachment_type == "Image":
            uploaded_image = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
            if uploaded_image:
                attachment_path = Path("uploaded_image." + uploaded_image.name.split(".")[-1])
                with open(attachment_path, "wb") as f:
                    f.write(uploaded_image.read())

        elif attachment_type == "PDF":
            uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
            if uploaded_pdf:
                attachment_path = Path("uploaded_pdf.pdf")
                with open(attachment_path, "wb") as f:
                    f.write(uploaded_pdf.read())

        # Send email button
        if st.button("Send Email"):
            if recipient and subject and body:
                for index, row in df.iterrows():
                    send_email(row['email'], subject, body, attachment_path)
                st.success("Emails sent successfully!")

if __name__ == "__main__":
    main()
