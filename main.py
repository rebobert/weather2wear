
#www.visualcrossing.com

# import all necessary modules
import streamlit as st
import requests
import json
import datetime
import pytz
import os, sys
import base64
from datetime import timedelta, datetime
from streamlit_lottie import st_lottie
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from streamlit_option_menu import option_menu


# declare variables
itemLists = []
tempDifference = 0

# add background image to main page
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

# main function calls all other functions and collects data
def main():
  st.markdown("<h1 style='text-align: center; font-size:100px;'><span style='color: orange;'>&#x2600;</span></h1>", unsafe_allow_html=True)     
  st.markdown("<h1 style='text-align: center; font-size:50px; color: black;'>Weather 2 Wear </h1>", unsafe_allow_html=True)
  st.markdown("<h1 style='text-align: center; font-size:30px; color: black;'>Stay Comfortable, Whatever the Weather</h1>", unsafe_allow_html=True)
  
  # User input, get weather data, get time information. 
  currentCity, pastCity = userPreference()
  dailyValues, currentConditions, hourlyWeather = apiCall(currentCity)

  if st.button("Get Clothing Recommendations"):
    if currentCity:
      st.write('')
      currentTime, currentIndex = getTime(hourlyWeather, currentCity)
      # Do weather calculations 
      tempDifference = weatherCalculation(currentCity, pastCity)
      maxTemp, maxTempIndex = getMinMaxTemp(dailyValues, hourlyWeather, currentIndex)
      avgTemp, avgWindchill = getAvgTemp(hourlyWeather, currentIndex)
      avgWind = getAvgWind(hourlyWeather, currentIndex)
      avgDewpoint = getAvgDewpoint(hourlyWeather, currentIndex)
      hourlyPrecipList, hourlyPrecipIndex = getPrecip(currentIndex, dailyValues, hourlyWeather)

      # Clothing related functions
      clothingData = openFile()
      # Go through all of the categories (temperature, wind, dewpoint,
      # precipitation and reduce the list of available clothing items)
      for itemType in list(clothingData.keys()):
          itemCategoryList = getItemTemp(tempDifference, itemType, clothingData, avgTemp)
          itemCategoryList = getItemWind(itemCategoryList, avgWind)
          itemCategoryList = getItemDewpoint(itemCategoryList, avgDewpoint)
          itemCategoryList = getItemPrecip(itemCategoryList,
                                          hourlyPrecipList, hourlyPrecipIndex)
          itemLists.append(itemCategoryList)

        
        
      # once all clothing items have been reduced, find best and print
      findBestItem(itemCategoryList, avgTemp)

      st.markdown("<h1 style='font-size:25px; color: #1D375D;'>Today's Weather</h1>", unsafe_allow_html=True)
      
      st.write("Current time in", currentCity, "is", currentTime)
      st.write("\nHighest Temperature:", str(maxTemp) + u"\u2103" + "  at", str(maxTempIndex) + ":00")
      # Print valuable data for user for the whole day. 
      st.write('Average Temperature:', str(round(avgTemp, 1)) + u"\u2103")
      st.write('Average \'Feels Like\':', str(round(avgWindchill, 1)) + u"\u2103")
      st.write('Average Windspeed:', str(round(avgWind, 1)) + 'km/h')
      st.write('Average Dewpoint:', str(round(avgDewpoint, 1)) + u"\u2103" '\n')
      # check if the precipitation will be less than 1cm 
      # and probability will be less than 10%
      if dailyValues['precip'] < 1 and dailyValues['precipprob'] < 20:
          st.write("\nThere is not predicted to be any precipitation today\n")
    else:
      st.warning('Please enter your city name')
    
  #Resize and center align image
  st.write('\n\n\n\n ')
  st.write(' ')
  left, middle, right = st.columns(3)
  with left:
      st.image('./PoweredByVC-WeatherLogo-RoundedRect.png', width=100)
      st.markdown("[![Foo]('./PoweredByVC-WeatherLogo-RoundedRect.png')](https://www.visualcrossing.com/weather-api)")
      st.markdown(![Foo](./PoweredByVC-WeatherLogo-RoundedRect.png))

# Call the weather API from visual crossing for the current weather data. 
def apiCall(currentCity):
  try:
    api =   f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{currentCity}/today?unitGroup=metric&key=HV4MB4NPS3KVP4YMCVPZYG3QD&contentType=json"
    # Call API and store data in result, then load the txt into a json called result.
    apidata = requests.get(api)
    result = json.loads(apidata.text)
    # Get the days calculated from the API, the current conditions and all hourly
    # values from the current day.
    dailyValues = result['days'][0]
    currentConditions = result['currentConditions']
    hourlyWeather = dailyValues['hours']
  except json.decoder.JSONDecodeError:
    st.warning('Please enter valid city name')
    exit()

  return dailyValues, currentConditions, hourlyWeather

# Get current time and find index to start searches from.
# https://www.programiz.com/python-programming/datetime/current-time
def getTime(hourlyWeather, currentCity):
  #timezone = pytz.timezone('America/Edmonton')
  
  geolocator = Nominatim(user_agent='myGeocoder')
  location = geolocator.geocode(currentCity)
  tf = TimezoneFinder()
  latitude, longitude = location.latitude, location.longitude
  timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
  timezone = pytz.timezone(timezone_str)
  currentTime = datetime.now(timezone).strftime("%H:%M:%S")
  for hour in hourlyWeather:
    if hour['datetime'][0:2] == currentTime[0:2]:
      currentIndex = hourlyWeather.index(hour)
  return currentTime, currentIndex
  


# Get the min/max temperature and their time. 
def getMinMaxTemp(dailyValues, hourlyWeather, currentIndex):  
  #set maxTemp
  maxTemp = -100
  for hour in hourlyWeather[currentIndex:]:
    if float(hour['temp']) > maxTemp:
      maxTemp = hour['temp']
      maxTempIndex = hourlyWeather.index(hour)
  return(maxTemp, maxTempIndex)


# Gather various information from the user which will assist in providing accurate clothing selection. 
def userPreference():
  # Source for json: https://github.com/samayo/country-json/blob/master/src/country-by-capital-city.json
  # attempt to open json file and load data
    try:
      countryCityFile = open("countries_and_cities.json")
    except:
      st.warning("Unable to open countries and cities information")
      exit()

    countryCityData = json.load(countryCityFile)

  # get city information from user.
    text_input = """
    <style>
    div[class*="stTextInput"] label p {
      font-size: 20px;
      color: black;
    }
    </style>
    """
    st.write(text_input, unsafe_allow_html=True)
    
    currentCity = st.text_input("Enter City", placeholder='Hit enter to apply')
    pastCity = None

    if currentCity:
      yesNo = st.radio(f"(Optional) Are you travelling from another city?", ('No', 'Yes'))
      if yesNo == 'No':
        #if user is in city they've lived in, continue. 
        return currentCity, currentCity
      elif yesNo == 'Yes':
        #if user is in different climate, ask which country. 
          pastCity = st.text_input("Enter Previous City", placeholder='Hit enter to apply')
          return currentCity, pastCity
    return None, None


#Calculate the difference in average temperature between 
def weatherCalculation(currentCity, pastCity):
  #Get current date and 6 months ago. 
    if currentCity == pastCity:
        tempDifference = 0
        return tempDifference
    geolocator = Nominatim(user_agent='myGeocoder')
    location = geolocator.geocode(currentCity)
    tf = TimezoneFinder()
    latitude, longitude = location.latitude, location.longitude
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
    timezone = pytz.timezone(timezone_str)  
    currentTime = datetime.now(timezone).strftime("%H:%M:%S")
    today = datetime.today().strftime('%Y-%m-%d')
    six_months_ago = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
    # Call API with each city and time information.
    pastCityApi = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{pastCity}/{six_months_ago}/{today}?unitGroup=metric&elements=datetime%2Ctemp%2Cfeelslike&include=days&key=HV4MB4NPS3KVP4YMCVPZYG3QD&contentType=json"
    currentCityApi = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{currentCity}/{six_months_ago}/{today}?unitGroup=metric&elements=datetime%2Ctemp%2Cfeelslike&include=days&key=HV4MB4NPS3KVP4YMCVPZYG3QD&contentType=json"
    # Put the API called data into a readable json. 
    pastApiData = requests.get(pastCityApi)
    pastResult = json.loads(pastApiData.text)
    currentApiData = requests.get(currentCityApi)
    currentResult = json.loads(currentApiData.text)  

    # Get the days calculated from the API, the current conditions and all hourly
    # values from the calculated days.
    pastCityTemps = pastResult['days']
    currentCityTemps = currentResult['days']
    n = 0
    temp = 0
    #Get the average feels like temp from the calculated amount of time. Divide total temperature by number of days calculated. 
    for day in pastCityTemps:
        temp += int(day['feelslike'])
        n += 1
    pastCityAvgTemp = temp / n 
    n = 0
    temp = 0
    for day in currentCityTemps:
        temp += int(day['feelslike'])
        n += 1
    currentCityAvgTemp = temp / n
    # check if it's warmer or colder here, assign temp difference
    # negative value if the current city is colder, 
    # positive value if the current city is warmer
    tempDifference = currentCityAvgTemp - pastCityAvgTemp
    
    if tempDifference != 0:
        st.markdown("<h1 style='font-size:25px; color: #1D375D;'>Temperature Difference</h1>", unsafe_allow_html=True)
        st.write("Average temperature for past 30 days in", pastCity, "is", 
              str(round(pastCityAvgTemp, 1)) + u"\u2103")
        st.write("Average temperature for past 30 days in", currentCity, "is",     
              str(round(currentCityAvgTemp, 1)) + u"\u2103")
    # Print temperature difference over past month
        # negative value if the current city is colder, 
        # positive value if the current city is warmer
    if currentCityAvgTemp > pastCityAvgTemp:
          st.write(currentCity, "is", str(abs(round(tempDifference, 1))), "degrees warmer than", pastCity, "over the past month.")
    else:
          st.write(currentCity, "is", str(abs(round(tempDifference, 1))), "degrees colder than", pastCity, "over the past month.")
      
    return tempDifference

def getAvgTemp(hourlyWeather, currentIndex):
#Get average temperature and windchill for rest of the day
    avgTemp = 0
    avgWindchill = 0
    for hour in hourlyWeather[currentIndex:]:
        avgTemp += hour['temp'] / (24-currentIndex)
    for hour in hourlyWeather[currentIndex:]:
        avgWindchill += hour['feelslike'] / (24-currentIndex)
    return avgTemp, avgWindchill

def getAvgWind(hourlyWeather, currentIndex):
    avgWind = 0
    for hour in hourlyWeather[currentIndex:]:
        avgWind += hour['windspeed'] / (24 - currentIndex)
    return avgWind

def getAvgDewpoint(hourlyWeather, currentIndex):
    avgDewpoint = 0
    for hour in hourlyWeather[currentIndex:]:
        avgDewpoint += hour['dew'] / (24 - currentIndex)
    return avgDewpoint
  
# Get precipitation values from API and provide them in a list. 
def getPrecip(currentIndex, dailyValues, hourlyWeather):
    # check if the precipitation will be less than 1cm 
    # and probability will be less than 10%
    if dailyValues['precip'] < 1 and dailyValues['precipprob'] < 20:
        return [0], [0]
    # code only runs if above code does not apply.
    precipType = dailyValues['preciptype']
    hourlyPrecipList = []
    hourlyPrecipIndex = []
    # go through each hour remaining in the day, add the precipitation values (in mm)
    # along with their index (hour)
    for hour in hourlyWeather[currentIndex:]:
        hourlyPrecipList.append(hour['precip'])
        hourlyPrecipIndex.append(hourlyWeather.index(hour))
    return hourlyPrecipList, hourlyPrecipIndex
  
#Get appropriate clothing items for average temperature of the day
def getItemTemp(tempDifference, itemType, clothingData, avgTemp):
    
    n = 0
    list = []
    # check if values 
    for item in clothingData[itemType]:
        if int(clothingData[itemType][n]['minTemp']) <= avgTemp <= int(clothingData[itemType][n]['maxTemp']):
            min = int(item.get('minTemp'))
            max = int(item.get('maxTemp'))
            list.append(item)
        n += 1
    return list

def getItemWind(itemCategoryList, avgWind):
    n = 0
    # go through all the items, if item is removed, remain at same index
    # to prevent skipping items. 
    while n < len(itemCategoryList):
        # if item max wind lower than average wind, remove. 
        if int(itemCategoryList[n]['maxWind']) <= avgWind:
            itemCategoryList.remove(itemCategoryList[n])
        # move to next 
        else:
          n += 1
    return itemCategoryList

def getItemDewpoint(itemCategoryList, avgDewpoint):
    
    n = 0
    # go through all the items, if item is removed, remain at same index
    # to prevent skipping items. 
    while n < len(itemCategoryList):
        # if item max wind lower than average wind, remove. 
        if int(itemCategoryList[n]['maxDewpoint']) <= avgDewpoint:
            itemCategoryList.remove(itemCategoryList[n])
        # move to next 
        else:
          n += 1
    return itemCategoryList

def getItemPrecip(itemCategoryList, hourlyPrecipList, hourlyPrecipIndex):
    n = 0
    while n < len(itemCategoryList):
        # check each hour in the precip, if the min is higher than precip
        # or max is lower than precip, remove. 
        for hourPrecip in hourlyPrecipList:
            if int(itemCategoryList[n]['minPrecip']) > hourPrecip or int(itemCategoryList[n]['maxPrecip']) < hourPrecip:
                itemCategoryList.remove(itemCategoryList[n])
                n -= 1
                break
        n += 1
    return itemCategoryList
  
#locate the best item in each clothing category
def findBestItem(itemList, avgTemp):
  # check if shirts and bottoms are recommended, if not, exit.
  if itemLists[4] == [] and itemLists[7] == []:
      st.warning("The application currently does not support extreme weather conditions")
      return
  st.markdown("<h1 style='font-size:25px; color: #1D375D;'>Today's Recommendations</h1>", unsafe_allow_html=True)
  for itemList in itemLists:
        bestItemTemp = 100
        bestItem = {}
        for item in itemList:
            itemAverageTemp = (int(item.get('minTemp'))+
                              int(item.get('maxTemp')))/2
            if abs(abs(itemAverageTemp)-abs(avgTemp)) < bestItemTemp:
                bestItem = item
        # check if item is none value, if not, print to user. 
        bestItemName = bestItem.get('name')
        if not bestItemName == None:
            itemNameURL = bestItemName.replace(" ", "+")
            itemURL = f'https://www.google.com/search?tbm=shop&hl=en&psb=1&ved=2ahUKEwi3rIOgwIyAAxXgzsIEHaFCArMQu-kFegQIABAK&q={itemNameURL}&sclient=products-cc'
            st.markdown(
            f'''
            <a href="{itemURL}" title="{bestItemName}"><button style="background-color:White;">{bestItemName}</button></a>
            ''',
            unsafe_allow_html=True)
      
#Import the clothing item json file into the main.py
def openFile():
    try:
       file = open("clothing_new.json")
    except:
       st.warning("Cannot open clothing data")
    clothingData = json.load(file)
    
    return clothingData

main()
