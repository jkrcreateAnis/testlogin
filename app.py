import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc6749.errors import OAuthError

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

    # Get the authorization URL and state
    authorization_url, state = oauth.create_authorization_url(authorization_base_url)

    # Redirect user to Google login page
    st.markdown(f'<a href="{authorization_url}" target="_blank">Click here to log in with Google</a>', unsafe_allow_html=True)

    # After user logs in, Google will redirect back to this app with the authorization code
    authorization_response = st.query_params
    
    if 'code' in authorization_response:
        try:
            token = oauth.fetch_token(token_url, authorization_response=authorization_response)
            st.session_state.logged_in = True
            st.session_state.token = token
            user_info = oauth.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
            st.session_state.username = user_info['name']  # You can store more user info here
            st.success(f"Hello, {st.session_state.username}!")
            
            # Redirect to the main app page after successful login
            st.session_state.redirect_to_main = True
        except OAuthError as e:
            st.error(f"An error occurred while fetching the token: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Main page logic
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    login_screen()
else:
    if "redirect_to_main" in st.session_state and st.session_state.redirect_to_main:
        # After login, redirect to the main content page
        st.experimental_set_query_params(page="main")  # Optional: Pass a query parameter if needed
        st.experimental_rerun()  # Or use another method like st.redirect()
    
    # Main app page content after login
    st.header(f"Selamat Datang, {st.session_state.get('username', 'User')}!")
    st.write("You are successfully logged in. Here's the main content of the app.")
    
    # Add some main app features, e.g., a button or some data visualization
    st.button("View Dashboard")
    st.write("Here you can access the system's dashboard or other features.")
    
    # Log out button to clear the session
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.token = ""
        st.session_state.redirect_to_main = False
        st.experimental_rerun()
