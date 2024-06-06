import os

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px #install plotly and use it for the analysis in page 1
from geopy.geocoders import Nominatim   #import geopy for writing the programme to locate places
#TO LOAD EXCEL DATA SET YOU MUST INSTALL pip install openpyxl


# CREATING DATABASE AND TABLEs HERE
from PIL import Image

db_path = os.getcwd() + '//db//mydb.db'
conn = sqlite3.connect(db_path)
#create tables
def create_db():
    try:
        #create user table
        conn.execute(
            'CREATE TABLE IF NOT EXISTS users_table (User_ID INTEGER PRIMARY KEY AUTOINCREMENT, Email VARCHAR, username, Password VARCHAR, Reg_Date)')
        st.success('User Table Created successfully')
    except sqlite3.Error as error:
        print('error while connecting to db', error)
    finally:
        conn.close()

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

#OPENING THE CSS
with open('mystyle/app_style.css') as  f:
    css = f.read()


#Get your username and password variable which could come from database
uname = "admin"
pwd = "123"

#st.image('analysis_img/girl.jpg') #Working image loading

#configuring the page along with the tab icon
st.set_page_config(page_title="Superstore Analysis", page_icon=":chart_with_upwards_trend:", layout="wide")
#main function to run the app
def main():
    st.title("Streamlite App with Login Page")
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True) #Connecting to the external css

    #initialize session state in the main to be used for login
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] =False


    #Creating Login Form
    if not st.session_state['logged_in']:
        st.subheader('please contact admin for login details')
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
                # call create
                create_db()
                st.rerun()  #Reload the Page so that the login page will go away for the home page to appear

                #if username does not match display error message
            else:
                st.error("Invalid username or password")



    #PROTECTED CONTENTS STARTS HERE

    #Show content if logged in

    if st.session_state['logged_in']:
        sidebar = st.sidebar.write(f"Welcome, {st.session_state['username']}")  # shows username on the sidebar

        #column
        #sidebar = st.sidebar.write("side bar")  # shows username on the sidebar
        st.sidebar.write(st.session_state['username']) #just getting the username of the logged in user
        st.sidebar.image('analysis_img/logo.png') #Adding picture on the side bar

        # Adding Logout button on the side bar and using it to Logout user When clicked
        if st.sidebar.button("Log out"):
            st.session_state['logged_in'] = False

            # MAKES THE APP TO RELOAD WHEN LOGGED OUT
            st.rerun()


        #Adding select box on the Sidebar
        page = st.sidebar.selectbox("Select a page", ["Analysis Page 1", "Get Location", "Page 3", "Create-acc"]) #Add to side bar

        #Checking to determine the pages
        if page =="Analysis Page 1":
            st.write("Welcome to ANALYSIS Page (ANALYSING TOTAL SALES BY CITY AND STATE")

            # Sample data
            data = {
                "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
                "State": ["NY", "CA", "IL", "TX", "AZ"],
                "Sales": [250000, 200000, 150000, 120000, 100000],
                "Latitude": [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
                "Longitude": [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740]
            }
            df = pd.DataFrame(data)
            # sHOW DATAFRAME
            st.write("Data Table")
            st.write(df)

            #MAP ANALYSIS ON THE SAME COLUMN

            # Analysis using map plot
            st.subheader("Total Sales by City")
            # Option to select state or city
            view_by = st.selectbox("View by", ["State", "City"])
            if view_by == "State":
                # Aggregate sales by state
                state_sales = df.groupby("State").sum().reset_index()  # summing all the sales

                # Create map
                fig = px.choropleth(
                    state_sales,
                    locations="State",
                    locationmode="USA-states",
                    color="Sales",
                    scope="usa",
                    title="Total Sales by State"

                )
                st.plotly_chart(fig)
            else:
                # Create scatter map for cities
                fig = px.scatter_mapbox(
                    df,
                    lat="Latitude",
                    lon="Longitude",
                    size="Sales",
                    color="Sales",
                    hover_name="City",
                    hover_data=["State", "Sales"],
                    zoom=3,
                    mapbox_style="carto-positron",
                    title="Total Sales by City"
                )
                st.plotly_chart(fig, use_container_width=True)



        #Another Page

        elif page == "Get Location":
            st.write("Welcome to ANALYSIS Page 2 where you enter City and State to get the Longitude and Latitude")

            #GET LONGITUDE VALUES FROM STATES NAME SPECIFIED AND USE IT FOR YOUR Analysis with Longitude and Latitude
            def geocode_locations(locations):
                geolocator = Nominatim(user_agent="streamlit-app")
                latitudes = []
                longitudes = []

                for location in locations:
                    try:
                        loc = geolocator.geocode(location)
                        if loc:
                            latitudes.append(loc.latitude)
                            longitudes.append(loc.longitude)
                        else:
                            latitudes.append(None)
                            longitudes.append(None)
                    except Exception as e:
                        latitudes.append(None)
                        longitudes.append(None)
                return latitudes, longitudes

            # Title the chart Area
            st.title("Geocode Locations and Display on Map")

            #Get Location using Form
            st.subheader('Please Put your Locations here, Each in a new Line')
            with st.form("Collect Locations"):
                st.write("Collect Locations to Generate the Latitude and Longitude")
                locations_names = st.text_area("Enter Each Location in a New line")
                submit_button = st.form_submit_button("Submit Location List")

                #Check when form is clciced
                if submit_button:
                    get_locations = [loc.strip() for loc in locations_names.split('\n') if loc.strip()]
                    get_latitudes, get_longitudes = geocode_locations(get_locations)
                    # Create DataFrame
                    df1 = pd.DataFrame({
                        "Location": get_locations,
                        "Latitude": get_latitudes,
                        "Longitude": get_longitudes
                    })

                    # Display DataFrame
                    st.write("Geocoded Locations")
                    st.write(df1)

                    # Filter out locations with missing coordinates
                    df1 = df1.dropna(subset=["Latitude", "Longitude"])

                    # Create map
                    fig1 = px.scatter_mapbox(
                        df1,
                        lat="Latitude",
                        lon="Longitude",
                        hover_name="Location",
                        zoom=4,
                        mapbox_style="carto-positron",

                    )

                    st.plotly_chart(fig1)

                #USING FORM TO COLLECT THE LOCATIONS ENDS HERE





            #COLLECTING FROM THE TEXT AREA DIRECTLY WITHOUT USING FORM
            # Analysis with Longitude and Latitude
            def geocode_locations(locations):
                geolocator = Nominatim(user_agent="streamlit-app")
                latitudes = []
                longitudes = []

                for location in locations:
                    try:
                        loc = geolocator.geocode(location)
                        if loc:
                            latitudes.append(loc.latitude)
                            longitudes.append(loc.longitude)
                        else:
                            latitudes.append(None)
                            longitudes.append(None)
                    except Exception as e:
                        latitudes.append(None)
                        longitudes.append(None)
                return latitudes, longitudes

            # Streamlit app
            st.title("Geocode Locations and Display on Map")

            # Input locations (cities or addresses)
            locations_input = st.text_area("Enter locations (one per line)", "New York\nLos Angeles\nChicago")
            # Process input
            locations = [loc.strip() for loc in locations_input.split('\n') if loc.strip()]

            # Geocode locations
            latitudes, longitudes = geocode_locations(locations)

            # Create DataFrame
            df = pd.DataFrame({
                "Location": locations,
                "Latitude": latitudes,
                "Longitude": longitudes
            })

            # Display DataFrame
            st.write("Geocoded Locations")
            st.write(df)

            # Filter out locations with missing coordinates
            df = df.dropna(subset=["Latitude", "Longitude"])

            # Create map
            fig = px.scatter_mapbox(
                df,
                lat="Latitude",
                lon="Longitude",
                hover_name="Location",
                zoom=3,
                mapbox_style="carto-positron"
            )

            st.plotly_chart(fig)






        elif page == "Page 3":
            st.write("ANALYSIS WITH DATA THAT HAS ONLY STATE OR CITY, WE GENERATE LAT AND LON IN PYTHON FOR MAP")

            df = pd.read_excel('dataset/sales.xlsx')  # for reading excel file
            st.write("Imported Data set")
            #ORIGINAL DATASET
            df

            # COLLECTING FROM THE TEXT AREA DIRECTLY WITHOUT USING FORM
            # Analysis with Longitude and Latitude
            def geocode_locations(locations):
                geolocator = Nominatim(user_agent="streamlit-app")
                latitudes = []
                longitudes = []

                for location in locations:
                    try:
                        loc = geolocator.geocode(location)
                        if loc:
                            latitudes.append(loc.latitude)
                            longitudes.append(loc.longitude)
                        else:
                            latitudes.append(None)
                            longitudes.append(None)
                    except Exception as e:
                        latitudes.append(None)
                        longitudes.append(None)
                return latitudes, longitudes

            # tITLING MY GEOLOCATIONS DISPLAY ON MAP
            st.title("Geocode Locations and Display on Map")

            #GET LOCATION STATES FROM MY DATASET COLUMN STATE
            locations_input_dataset = df["state"]

            # Process / GET LOCATION OF PLACES ON THE MAP USING THE STATES PROVIDED ABOVE
            locations = [loc.strip() for loc in locations_input_dataset]

            # Geocode locations (Get the lontitude and latitude of states positions on the map
            latitudes, longitudes = geocode_locations(locations)

            # Add LATITUDE AND LONGITUDE VALUES TO MY DATAFRAME DF (ADDING NEW COLUMS)
            df['Latitude'] = latitudes
            df['Longitude'] = longitudes

            #VIEW THE NEW DATASET
            df

            #CALCULATING TOTAL SUM OF SALES (this will form our new dataframe
            df_state_sales = df.groupby("state").sum().reset_index()  # summing all the sales

            #SHOW THE NEW DATAFRAME ON THE PAGE
            st.write("Total sales grouped by state")
            st.write(df_state_sales)

            # Create map
            fig = px.scatter_mapbox(
                df_state_sales,
                hover_data="sales",
                hover_name="state",
                lat="Latitude",
                lon="Longitude",
                zoom=4,
                mapbox_style="carto-positron"
            )

            st.plotly_chart(fig)











            #Adds text on the side bar when this page is loaded
            st.sidebar.write("Am in side bar")
        elif page == "Create-acc":
            st.title("Create Account")
            if st.session_state['logged_in']:

                #Creating Account form
                with st.form("Create Account Form"):
                    st.write("Please log in")
                    username = st.text_input("Username")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    reg_date = st.date_input("Registration date")
                    create_acc_button = st.form_submit_button("Create account")

                if create_acc_button:
                    #Get User Details and Insert Data Into the user Table
                    try:
                        with sqlite3.connect(db_path) as conne:
                            cur = conne.cursor()
                            cur.execute("INSERT INTO users_table (Email, username, password, reg_date) VALUES (?,?,?,?)",
                                    (email, username, password, reg_date))
                            conne.commit()
                            st.success('user Account Created Successfully')
                    except sqlite3.Error as err:
                        conne.rollback()
                        print("error occured during Account Creation", err)




#Run the App
if __name__ == "__main__":
    main()