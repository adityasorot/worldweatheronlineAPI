import pandas as pd
import requests

# data with columns as ('latitude','longitude','month_no','year')
data=pd.read_csv('data.csv')
data['lon_r']=data['lon'].round(3) # the api takes value with three decinal value
data['lat_r']=data['lat'].round(3)
data_1 = data[['month','year','lon_r','lat_r']]
s1 = data_1.drop_duplicates(ignore_index=True) # dropping duplicates, you don't wanna waste the api calls

# takes the json and extract the values as a list
def get_value(json):
    maxtempC=json['data']['weather'][0]['maxtempC']
    mintempC=json['data']['weather'][0]['mintempC']
    avgtempC=json['data']['weather'][0]['avgtempC']
    windspeedKmph=json['data']['weather'][0]['hourly'][0]['windspeedKmph']
    humidity=json['data']['weather'][0]['hourly'][0]['humidity']
    listofdata=[maxtempC,mintempC,avgtempC,windspeedKmph,humidity]
    return listofdata

lon=list(s1['lon_r'])
lat=list(s1['lat_r'])
mon=list(s1['month'])
year=list(s1['year'])
info=list(zip(lat,lon,mon,year))
key='XXXXXXXXXXXXXXXXXXXXXX' # Your api key
finallist=[]

for lat,lon,mon,year in info:
    lop=str(lat)+','+str(lon)+
    date=str(year)+'-'+str(mon)+'-15'
    while True: # get only valid response
        response = requests.get(f"http://api.worldweatheronline.com/premium/v1/past-weather.ashx?q={lop}&date={date}&format=json&key={key}")
        if response.status_code == 200:
            break
        else:
            continue
    listofdata=get_value(response.json())
    finallist.append(listofdata) # add data to the lisy

dataframe=pd.DataFrame(finallist,columns=['maxtempC','mintempC','avgtempC','windspeedKmph','humidity']) # append data to the dataframe
dataframe=pd.concat([s1, dataframe], axis=1)
