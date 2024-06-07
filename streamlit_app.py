import streamlit as st
import json
from google.cloud import storage
from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import GenerativeModel

# Function to create service account credentials from st.secrets
def get_service_account_credentials():
    service_account_info = {
        "type": st.secrets["google_cloud"]["type"],
        "project_id": st.secrets["google_cloud"]["project_id"],
        "private_key_id": st.secrets["google_cloud"]["private_key_id"],
        "private_key": st.secrets["google_cloud"]["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["google_cloud"]["client_email"],
        "client_id": st.secrets["google_cloud"]["client_id"],
        "auth_uri": st.secrets["google_cloud"]["auth_uri"],
        "token_uri": st.secrets["google_cloud"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google_cloud"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["google_cloud"]["client_x509_cert_url"],
        "universe_domain": st.secrets["google_cloud"]["universe_domain"]
    }
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    return credentials

# Initialize a Google Cloud Storage client
credentials = get_service_account_credentials()
client = storage.Client(credentials=credentials)

def multiturn_generate_content(text):
    vertexai.init(project="537000417203", location="us-central1")
    model = GenerativeModel(
    "projects/537000417203/locations/us-central1/endpoints/7732880671311396864",
    )
    chat = model.start_chat()

    generation_config = {
        "max_output_tokens": 2048,
        "temperature": 1,
        "top_p": 1,
    }
    try:
        response = chat.send_message(
            [text + " Write in the style of the person who you were finetuned on and don't talk about you. Write 300-500 words"],
            generation_config=generation_config,
        )
        st.write(response)
        return response
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

def streamlit_app():
    # Title of the webpage
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
            response = multiturn_generate_content(user_input)
            if response:
                st.write(response)
                response_dict = response.to_dict()
                content = response_dict['candidates'][0]['content']['parts'][0]['text']
                st.write(content.encode().decode('unicode_escape'))

if __name__ == "__main__":
    streamlit_app()