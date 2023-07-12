'''
import streamlit as st
from streamlit_option_menu import option_menu


def home():
    st.title("Home Page")
    if st.button('Click for Weather Information'):
        st.session_state['selected'] = 'Weather Information'
        st.experimental_rerun()

def weather_info():
    st.title("Weather Information Page")
    if st.button('Back to menu'):
        st.session_state['selected'] = 'home'
        st.experimental_rerun()

def clothing_recommendation():
    st.title("Clothing Recommendation Page")
    
with st.sidebar:

    selected = option_menu(

        menu_title='Menu', 
        menu_icon="cast",
        options=["Home", "Weather Information", "Clothing Recommendation"],
        icons=["house", "book", "envelope"],
        default_index=0
    )


if 'selected' not in st.session_state:
    st.session_state['selected'] = 'Home'

if 'selected' in st.session_state:
    selected = st.session_state['selected']

    
if selected == "Home":
    home()
if selected == "Weather Information":
    weather_info()
if selected =="Clothing Recommendation":
    clothing_recommendation()
'''
'''
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime, timedelta

geolocator = Nominatim(user_agent='myGeocoder')
location = geolocator.geocode('calgary')
tf = TimezoneFinder()
latitude, longitude = location.latitude, location.longitude
timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
timezone = pytz.timezone(timezone_str)
ny_now = datetime.now(timezone)
print(datetime.today().strftime('%Y-%m-%d'))

'''
#print(datetime.today().strftime('%Y-%m-%d') - timedelta(days=2)).strftime('%Y-%m-%d')
'''
import streamlit as st
import streamlit.components.v1 as components

# embed streamlit docs in a streamlit app
components.iframe("https://docs.streamlit.io/en/latest", width=700, height=700, scrolling=True) 
'''

import streamlit as st
import streamlit.components.v1 as components

# bootstrap 4 collapse example
components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <div id="accordion">
      <div class="card">
        <div class="card-header" id="headingOne">
          <h5 class="mb-0">
            <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
            Collapsible Group Item #1
            </button>
          </h5>
        </div>
        <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
          <div class="card-body">
            Collapsible Group Item #1 content
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-header" id="headingTwo">
          <h5 class="mb-0">
            <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
            Collapsible Group Item #2
            </button>
          </h5>
        </div>
        <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
          <div class="card-body">
            Collapsible Group Item #2 content
          </div>
        </div>
      </div>
    </div>
    """,
    height=1000,
)