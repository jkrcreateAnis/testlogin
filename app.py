import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

# Function to create the login screen
def login_screen():
    st.header("Selamat Datang ke *e*-Sistem Jadual Kadar Kerja")
    st.subheader("Sila log masuk untuk meneruskan")
    
    if st.button("Daftar masuk dengan *Google Account*"):
        google_oauth_login()

def google_oauth_login():
    # Get the Google OAuth credentials from Streamlit secrets
    client_id = st.secrets["google"]["client_id"]
    client_secret = st.secrets["google"]["client_secret"]
    
    # Google OAuth2 configuration
    authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
    token_url = 'https://oauth2.googleapis.com/token'
    scope = 'openid profile email'

    # Redirect URI to your Streamlit Cloud app
    redirect_uri = "https://testesttest.streamlit.app/"  # Update to your deployed app URL

    # Initialize OAuth2 session
    oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri, scope=scope)

    # Get the authorization URL and state (use create_authorization_url instead of authorization_url)
    authorization_url, state = oauth.create_authorization_url(authorization_base_url)

    # Redirect user to Google login page
    st.markdown(f'<a href="{authorization_url}" target="_blank">Click here to log in with Google</a>', unsafe_allow_html=True)

    # After user logs in, Google will redirect back to this app with the authorization code
    authorization_response = st.query_params
    
    if 'code' in authorization_response:
        token = oauth.fetch_token(token_url, authorization_response=authorization_response)
        st.session_state.logged_in = True
        st.session_state.token = token
        user_info = oauth.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        st.session_state.username = user_info['name']  # You can store more user info here
        st.success(f"Hello, {st.session_state.username}!")

# Main page logic
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    login_screen()
else:
    st.header(f"Selamat Datang, {st.session_state.get('username', 'User')}!")
    st.button("Log keluar", on_click=lambda: st.session_state.update(logged_in=False))
