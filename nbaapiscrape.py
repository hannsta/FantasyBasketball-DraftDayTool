import requests
import json
import pickle

headers = {
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36'
}



##with open('gamecount.pickle', 'rb') as f:
 ##  i = pickle.load(f)
	
a = open('playersdump.txt', 'a')
i=1214
print(i)
while i < 1231:
	
	if i > 1000:
		shots_url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=28800&GameID=002120'+str(i)+'&RangeType=0&Season=2012-13&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
	if i < 1000:
		shots_url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=28800&GameID=0021200'+str(i)+'&RangeType=0&Season=2012-13&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
	if i < 100:
		shots_url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=28800&GameID=00212000'+str(i)+'&RangeType=0&Season=2012-13&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
	if i < 10:
		shots_url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=28800&GameID=002120000'+str(i)+'&RangeType=0&Season=2012-13&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'



	print(shots_url)
# request the URL and parse the JSON
	try:
		response = requests.get(shots_url,  headers=headers)
		response.raise_for_status() # raise exception if invalid response
		shots = response.json()['resultSets'][0]['rowSet']
		if shots:
			json.dump(shots, a)
			i += 1
		else:
			break
	except:
		print("....failed....")
		i += 1
#with open('gamecount.pickle', 'wb') as f:
#    pickle.dump(i, f)
