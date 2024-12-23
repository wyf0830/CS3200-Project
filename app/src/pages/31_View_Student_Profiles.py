# student_profile_app.py

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the title of the app
st.title("Student Profile Viewer")

# instructional text
st.write("Enter the **Student ID** to retrieve the student's profile information.")

# input field for Student ID
student_id = st.text_input("Student ID", value="", max_chars=10)

# button to get feedback
if st.button("Get Student Profile"):
    if student_id.strip() == "":
        st.error("Please enter a valid Student ID.")
    elif not student_id.isdigit():
        st.error("Student ID must be a numeric value.")
    else:
        # construct the API URL
        api_url = f"http://api:4000/ad/student/{student_id}"
        
        try:
            # send a GET request to the Flask API
            response = requests.get(api_url)
            
            if response.status_code == 200:
                # assuming the API returns a list of dictionaries
                data = response.json()
                
                if data:
                    # convert the data to a DataFrame for better display
                    df = pd.DataFrame(data)
                    
                    # display the DataFrame
                    st.success("Student Profile Retrieved Successfully!")
                    st.dataframe(df)
                else:
                    st.warning("No data found for the provided Student ID.")
            elif response.status_code == 404:
                st.warning("Student not found. Please check the Student ID and try again.")
            elif response.status_code == 500:
                st.error("Internal Server Error. Please try again later.")
            else:
                st.error(f"Unexpected error occurred. Status Code: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the API. Please ensure the Flask server is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")