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

st.title("About")
st.write('Welcome to Weather 2 Wear, your ultimate companion for staying comfortable and stylish, \
         no matter the weather! Our platform utilizes real-time weather data to provide personalized \
         clothing recommendations tailored to your specific location and climate conditions. ')

st.subheader('Why Weather 2 Wear?')
st.write('Weather can be unpredictable, and dressing appropriately for the conditions can make a \
         significant difference in your comfort level and overall experience. Our application takes \
         the guesswork out of dressing for the weather by analyzing various weather factors and \
         suggesting the best clothing items to suit your needs. From temperature and windchill \
         to precipitation and dew points, Weather 2 Wear considers all the critical factors that affect your clothing choices.')

st.subheader('How it works?')
st.write("1. Enter Your City: Simply enter your current location, and if you've recently traveled from another city, provide that information too.")
st.write('2. Get Weather Data: We retrieve real-time weather data for your location, including the current conditions and the forecast for the day.')
st.write('3. Clothing Recommendations: With the data in hand, we perform calculations to understand the temperature variations and potential weather changes. Then, we match the weather conditions to our extensive clothing database to recommend the most suitable clothing items for the day.')
st.write('4. Stay Comfy and Stylish: After considering various factors, including temperature, wind, dew point, and precipitation, Weather 2 Wear presents you with the best clothing choices that strike a perfect balance between comfort and style.')

st.subheader('Features and Benefits')
st.write('- Personalized Recommendations: Weather 2 Wear provides tailored clothing suggestions based on your location and weather conditions.')
st.write('- Real-Time Data: Our platform continuously updates weather information to ensure accurate recommendations for the current day.')
st.write('- Extensive Clothing Database: We have an extensive collection of clothing items to choose from, catering to all styles and preferences.')
st.write('- User-Friendly Interface: Our easy-to-use interface allows you to access clothing recommendations quickly and effortlessly.')

