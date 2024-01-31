import streamlit as st
import csv
from functions import *
from pathlib import Path

import yagmail
def read_csv_file(uploaded_file):
    try:
        data = uploaded_file.read().decode("utf-8")  
        reader = csv.DictReader(data.splitlines())
        return list(reader)
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")
        return None

def main():
    st.title("Send a lot of Emails")

    subject = st.text_input("Subject... Write something unusual")
    message = st.text_area("Write something that Gemini can edit. You don't need to write the full email yourself. Also, just tell the Niche of your Prospects to Gemini down the Variable")
    niche = st.text_input("Niche: ")
    autors = st.text_input("Enter the Copywriter you love | Copy his Style of Writing. ")
    st.write("I like Alex Cattoni Writing Style")

    uploaded_file = st.file_uploader("Upload a CSV file")
    
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

    if st.button("Fire the Emails!!!"):
        if uploaded_file is not None:
            contacts = read_csv_file(uploaded_file)

            if contacts is not None:
                for contact in contacts:
                    first_name = contact.get("First Name", "")
                    last_name = contact.get("Last Name", "")
                    company = contact.get("Company", "")
                    email = contact.get("Email", "")

                    response = model.generate_content([
                        f"Write an professional email within150 words  to {first_name} {last_name}\n\n"
                        f"search about this {company} so that you can make the message more personalized. "
                        f"The Niche of this company is {niche} You have to change the message such that it reflects "
                        f"the value of this company. Make sure to copy {autors} Style of Copywriting\n\n"
                        f"This is the Message:\n{message}\n\nThank you\n\n\nNOTE:Don't change the variables like "
                        f"|*FNAME*| or anything similar.\n\nDon't write any welcome messages like "
                        f"'I hope this message finds you well' because it looks usual. I want something unique\n\n"
                        f"Only Send the Email and don NOT include your text like 'Here is the Email'"
                        f"Warm Regards ,\n\n mention the senders name (Mr . Tapas ) and positions (CEO) from {niche}  "
                    ])
 

                    personalized_email = personalize_email(response.text, first_name, last_name, company)
                    send_email(email, subject, personalized_email ,attachment_path)
                    st.success("Emails sent successfully!")

if __name__ == "__main__":
    main()
