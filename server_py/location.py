import gpsd
import requests

# pip install gpsd-py3
def gpsloc(): # Connect to the local GPS daemon
    gpsd.connect()

    packet = gpsd.get_current()

    if packet.mode >= 2:
        latitude = packet.lat
        longitude = packet.lon
        print("Latitude:", latitude)
        print("Longitude:", longitude)
    else:
        print("GPS data not available.")

def iploc(): # Using IP Geolocation
    response = requests.get("https://ipinfo.io/json")
    data = response.json()

    if "loc" in data:
        latitude, longitude = data["loc"].split(",")
        print("Latitude:", latitude)
        print("Longitude:", longitude)
    else:
        print("Location not found.")

# gpsloc()
iploc()