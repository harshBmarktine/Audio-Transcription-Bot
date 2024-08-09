import streamlit as st
from audio_file_uploader import obj_audio_file_upload

# Sample user credentials
user_credentials = {
    "admin": "admin",
    "user2": "password2"
}



# Initialize session state if not already done
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

def speech_to_text():
    obj_audio_file_upload.audio_file()
def main():
    if not st.session_state.logged_in:
        st.title("Login Screen")

        # Input fields for username and password
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            if username in user_credentials and user_credentials[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                # Clear the screen after successful login
                st.rerun()
            else:
                st.error("Invalid username or password")
    else:
        st.title("Welcome")
        st.write(f"Welcome, {st.session_state.username}!")

        st.sidebar.image("https://marktine.com/wp-content/uploads/2024/07/marktine_new_logo.png", use_column_width=True)
        with st.sidebar:
            st.write("129, Shri Hans Marg, Usha Vihar, Keshav Vihar, Arjun Nagar, Jaipur, Rajasthan 302018")

        radio_button = {
            "Audio Transcription": speech_to_text
        }

        selected_page = st.sidebar.radio(" ", radio_button.keys())
        radio_button[selected_page]() # Clear the login screen after successful login
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            # Clear the screen after logout
            st.rerun()

if __name__ == "__main__":
    main()
