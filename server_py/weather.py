import requests

params = {
  'access_key': '9808f4fb16c77b55e002ae35f6a4ef02',
  'query': 'Ulaanbaatar'
}

api_result = requests.get('http://api.weatherstack.com/current', params)

api_response = api_result.json()

print(api_response)

# enkhsuren
# https://weatherstack.com/documentation
# https://weatherstack.com/dashboard

# https://www.visualcrossing.com/weather-api
print(u'Current temperature in %s is %d℃' % (api_response['location']['name'], api_response['current']['temperature']))