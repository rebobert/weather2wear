import streamlit as st
import base64

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/textStyle-left.css")

def background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()}); 
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
background('rb.png')

st.title("Legal Disclaimer")
st.write("Weather to Wear is an application that provides clothing recommendations based on forecasted weather conditions. These recommendations are intended as suggestions only and may not be accurate or suitable for every individual or for changing conditions.")
st.write("By using Weather to Wear, you acknowledge and agree to the following conditions:")
st.write("1. Limited Responsibility: Weather to Wear cannot be held responsible for changing weather conditions or inaccurate forecasts. Weather can change at any time and the user accepts full responsibility for their choice of clothing and any consequences arising from such choices.")
st.write("2. No Guarantee of Accuracy: Weather to Wear sources its weather data and information from a third-party source and cannot guarantee the accuracy or reliability of this data. Weather conditions can be unpredictable, and the app's recommendations may not always align perfectly with the actual conditions experienced.")
st.write("3. No Liability for Damages: In no event shall Weather to Wear or any affiliated individuals or agents be liable for any direct, indirect, incidental, consequential, natural, or special damages arising out of or in connection with the use of the app, including but not limited to damages for lost profits, damages to personal property, or any other intangible losses.")
st.write("4. User Responsibility and Discretion: The user takes full responsibility for verifying weather conditions through other sources and using their best judgement to select appropriate clothing. Weather to Wear suggests checking local weather forecasts, paying attention to weather alerts and warnings, and exercising caution when relying solely on Weather to Wear’s recommendations.")
st.write("By using Weather to Wear, you acknowledge that you have read, understood, and agreed to the terms and conditions outlined in this legal disclaimer. If you do not agree with any part of this disclaimer, please refrain from using Weather to Wear.")

st.subheader("Copyright")
st.write("©2023 Weather to Wear. All rights reserved.") 