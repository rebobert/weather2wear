import streamlit as st
import requests
import json
import datetime
import pytz

itemLists = []
tempDifference = 0

def apiCall(currentCity):
    api = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{currentCity}/today?unitGroup=metric&key=HV4MB4NPS3KVP4YMCVPZYG3QD&contentType=json"
    apidata = requests.get(api)
    result = json.loads(apidata.text)

    dailyValues = result['days'][0]
    currentConditions = result['currentConditions']
    hourlyWeather = dailyValues['hours']

    return dailyValues, currentConditions, hourlyWeather

def getTime(hourlyWeather):
    timezone = pytz.timezone('America/Edmonton')
    currentTime = datetime.datetime.now(timezone).strftime("%H:%M:%S")

    for hour in hourlyWeather:
        if hour['datetime'][0:2] == currentTime[0:2]:
            currentIndex = hourlyWeather.index(hour)

    return currentTime, currentIndex

def getMinMaxTemp(dailyValues, hourlyWeather, currentIndex):
    maxTemp = -100
    for hour in hourlyWeather[currentIndex:]:
        if float(hour['temp']) > maxTemp:
            maxTemp = hour['temp']
            maxTempTime = hour['datetime']

    return maxTemp, maxTempTime

def weatherCalculation(currentCity, pastCity):
    dailyValuesCurrent, _, hourlyWeatherCurrent = apiCall(currentCity)
    _, _, hourlyWeatherPast = apiCall(pastCity)

    avgTempCurrent, _, _, _ = getAvgTemp(hourlyWeatherCurrent, 0)
    avgTempPast, _, _, _ = getAvgTemp(hourlyWeatherPast, 0)

    return avgTempCurrent, avgTempPast

def getAvgTemp(hourlyWeather, currentIndex):
    totalTemp = 0
    totalWindchill = 0
    totalWindspeed = 0
    totalDewpoint = 0
    count = 0
    for hour in hourlyWeather[currentIndex:]:
        totalTemp += round(hour['temp'], 2)
        if 'windchill' in hour:
            totalWindchill += hour['windchill']
        if 'wspd' in hour:
            totalWindspeed += hour['wspd']
        if 'dew' in hour:
            totalDewpoint += round(hour['dew'], 2)
        count += 1
    avgTemp = round(totalTemp / count, 2)
    avgWindchill = totalWindchill / count if count > 0 else None
    avgWindspeed = totalWindspeed / count if count > 0 else None
    avgDewpoint = round(totalDewpoint / count if count > 0 else None, 2)
    return avgTemp, avgWindchill, avgWindspeed, avgDewpoint

def getItemTemp(tempDifference, itemType, clothingData, avgTemp):
    suitable_items = []
    
    for item in clothingData[itemType]:
        minTemp = int(item['minTemp'])
        maxTemp = int(item['maxTemp'])
        
        if minTemp <= (avgTemp + tempDifference) <= maxTemp:
            suitable_items.append(item)
            
    return suitable_items

def findBestItem(itemList, avgTemp):
    best_item = None
    best_diff = None
    
    for item in itemList:
        minTemp = int(item['minTemp'])
        maxTemp = int(item['maxTemp'])
        avg_item_temp = (minTemp + maxTemp) / 2

        temp_diff = abs(avgTemp - avg_item_temp)
        
        if best_item is None or temp_diff < best_diff:
            best_item = item
            best_diff = temp_diff

    return best_item

def openFile(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data

def get_weather_data(currentCity, pastCity):
    dailyValues, currentConditions, hourlyWeather = apiCall(currentCity)
    currentTime, currentIndex = getTime(hourlyWeather)

    avgTempCurrent, avgTempPast = weatherCalculation(currentCity, pastCity)
    tempDifference = avgTempCurrent - avgTempPast

    maxTemp, maxTempTime = getMinMaxTemp(dailyValues, hourlyWeather, currentIndex)
    avgTemp, avgWindchill, avgWindspeed, avgDewpoint = getAvgTemp(hourlyWeather, currentIndex)
    clothingData = openFile("clothing_new.JSON")

    bestItems = {}
    for itemType in list(clothingData.keys()):
        itemList = getItemTemp(tempDifference, itemType, clothingData, avgTemp)
        bestItems[itemType] = findBestItem(itemList, avgTemp)

    return currentTime, maxTemp, maxTempTime, avgTemp, avgWindchill, avgWindspeed, avgDewpoint, bestItems, avgTempCurrent, avgTempPast

if __name__ == "__main__":
    st.title("Weather to Wear")

    currentCity = st.text_input("What city are you in?")
    pastCityYN_placeholder = st.empty()
    pastCity_placeholder = st.empty()
    pastCity = None

    if currentCity:  # Check if currentCity is not empty
        pastCityYN = pastCityYN_placeholder.radio(f"Is {currentCity} in the country you've lived for the last 6 months?", ('Yes', 'No'))
        pastCity = currentCity
        
        if pastCityYN == 'No':
            pastCity = pastCity_placeholder.text_input("What country have you lived most in for the past 6 months?")
    
    if st.button("Get Clothing Recommendations"):
        if currentCity and pastCity and pastCityYN:
            pastCity = currentCity if pastCityYN == 'Yes' else pastCity
            currentTime, maxTemp, maxTempTime, avgTemp, avgWindchill, avgWindspeed, avgDewpoint, bestItems, avgTempCurrent, avgTempPast = get_weather_data(currentCity, pastCity)
            st.write(f"Current time is {currentTime}")
            st.write(f"Average temperature for {currentCity} is {avgTempCurrent}℃")
            st.write(f"Average temperature for {pastCity} is {avgTempPast}℃")
            st.write(f"The warmest of the day is {maxTemp}℃  at {maxTempTime}")
            st.write(f"Accounting for wind chill, it will feel like {avgWindchill}℃.")
            st.write(f"Average temperature for rest of the day is {avgTemp}℃")
            st.write(f"Average windchill for rest of the day is {avgWindchill}℃")
            st.write(f"Average windspeed for rest of the day is {avgWindspeed}km/h")
            st.write(f"Average  dewpoint for rest of the day is {avgDewpoint}℃")
            st.write("\nHere are some clothing recommendations for you today.")
            for itemType, item in bestItems.items():
                if item is not None:
                    st.write(f"For {itemType}, we recommend: {item['name']}")
                else:
                    st.write(f"No suitable {itemType} found for the current weather.")
        else:
            st.warning("Please input city information.")
        

st.write("")        
st.image('./PoweredByVC-WeatherLogo-RoundedRect.png')