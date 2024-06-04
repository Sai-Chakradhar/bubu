import streamlit as st
import os
import json





# Function to create a JSON file with service account credentials from st.secrets
def create_service_account_json():
    service_account_info = {
        "type": "service_account",
        "project_id": st.secrets["PROJECT_ID"],
        "private_key_id": st.secrets["PRIVATE_KEY_ID"],
        "private_key": st.secrets["PRIVATE_KEY"],
        "client_email": st.secrets["CLIENT_EMAIL"],
        "client_id": st.secrets["CLIENT_ID"],
        "auth_uri": st.secrets["AUTH_URI"],
        "token_uri": st.secrets["TOKEN_URI"],
        "auth_provider_x509_cert_url": st.secrets["AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": st.secrets["CLIENT_X509_CERT_URL"],
        "universe_domain": st.secrets["UNIVERSE_DOMAIN"]
    }
    with open('service_account.json', 'w') as json_file:
        st.write("True")
        json.dump(service_account_info, json_file)
    return 'service_account_info'

# Create the JSON file
    # Set the path to your service account key file if running locally
service_account_key_file = "service_account_info"


#service_account_key_file = create_service_account_json()

import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import os
from google.cloud import storage
from google.cloud import storage
from google.oauth2 import service_account

# Set the environment variable to point to your service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_key_file
# Initialize a Google Cloud Storage client
client = storage.Client()


#buckets = list(client.list_buckets())

def multiturn_generate_content(text):

    vertexai.init(project="363949151355", location="us-central1")
    model = GenerativeModel(
        "projects/363949151355/locations/us-central1/endpoints/5997868914866913280",
    )
    chat = model.start_chat()

    generation_config = {
        "max_output_tokens": 2048,
        "temperature": 1,
        "top_p": 1,
    }
    x = chat.send_message(
        [text + " Write in the style of the person who you were finetuned on and don't talk about you. Write 300-500 words"],
        generation_config=generation_config,
    )
    return x

def streamlit_app():
    # Title of the webpage
    st.write(service_account_key_file)
    st.title("Writer Project")
    
    st.subheader("Input a prompt and see it generate text in Kris Hammond's writing style")

    col1, col2 = st.columns(2)

    # Accept user input in the first column
    with col1:
        user_input = st.text_area("Enter your text here:", key="home_input")

    # Display the user input in the second column
    with col2:
        st.write("Generated text")
        if user_input:
            y = multiturn_generate_content(user_input)
            y = y.to_dict()
            content = y['candidates'][0]['content']['parts'][0]['text']
            st.write(content.encode().decode('unicode_escape'))
    
    

if __name__ == "__main__":
    streamlit_app()