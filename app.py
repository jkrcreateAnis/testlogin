import streamlit as st

# Function to create the login screen
def login_screen():
    st.header("Selamat Datang ke *e*-Sistem Jadual Kadar Kerja")
    st.subheader("Sila log masuk untuk meneruskan")
    
    # Google login button (you'll need to replace this with actual login code)
    if st.button("Daftar masuk dengan *Google Account*"):
        # Simulate a successful login (you can add actual login logic here)
        st.session_state.logged_in = True

# Main page logic
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    login_screen()
else:
    st.header(f"Selamat Datang, {st.session_state.get('username', 'User')}!")
    st.button("Log keluar", on_click=lambda: st.session_state.update(logged_in=False))
