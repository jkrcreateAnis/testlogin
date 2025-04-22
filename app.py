import streamlit as st

def login_screen():
    st.header("Selamat Datang ke *e*-Sistem Jadual Kadar Kerja")
    st.subheader("Sila log masuk untuk meneruskan")
    st.button("Daftar masuk dengan *Google Account*", on_click=st.login)
    
    
if not st.experimental_user.is_logged_in:
    login_screen()
else:
    st.header(f"Selamat Datang, {st.experimental_user.name}!")
    st.button("Log masuk", on_click=st.logout)
