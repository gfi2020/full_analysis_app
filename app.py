import streamlit as st
import pandas as pd
import numpy as np

#THEME
Blue = '''
    <style>
        .stApp {
        background-color: Blue;
        color: white;
    </style>
'''

Green = '''
    <style>
        .stApp {
        background-color: green;
        color: white;
    </style>
'''


#Get your username and password variable which could come from database
uname = "admin"
pwd = "123"


#main function to run the app
def main():
    st.title("Streamlite App with Login Page")

    #initialize session state in the main to be used for login
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] =False

    #Creating Login Form
    if not st.session_state['logged_in']:
        with st.form("Login_Form"):
            st.write("Please log in")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Log in")

        #Check when submit_button is pressed
        if submit_button:
            if (username == uname and password ==pwd):
                st.session_state['logged_in'] = True #sets login true
                st.session_state['username'] = uname    #Add username to session
                st.success("Logged in successfully")    #Display success message

                #Reload the Page so that the login page will go away for the home page to appear
                st.rerun()

                #if username does not match display error message
            else:
                st.error("Invalid username or password")



    #PROTECTED CONTENTS STARTS HERE

    #Show content if logged in
    if st.session_state['logged_in']:
        sidebar= st.sidebar.write(f"Welcome, {st.session_state['username']}") #shows username on the sidebar
        # Adding Logout button on the side bar and using it to Logout user When clicked
        if st.sidebar.button("Log out"):
            st.session_state['logged_in'] = False
            # MAKES THE APP TO RELOAD WHEN LOGGED OUT
            st.rerun()


        #Adding select box on the Sidebar
        page = st.sidebar.selectbox("Select a page", ["Page 1", "Page 2", "Page 3"]) #Add to side bar
        if page =="Page 1":
            st.write("Welcome to ANALYSIS Page 1")
        elif page == "Page 2":
            st.write("Welcome to ANALYSIS Page 2")
        elif page == "Page 3":
            st.write("Welcome to ANALYSIS Page 3")
            #Adds text on the side bar when this page is loaded
            st.sidebar.write("Am in side bar")



#Run the App
if __name__ == "__main__":
    main()