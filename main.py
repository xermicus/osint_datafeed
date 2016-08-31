import redis, time
from twython import Twython
from twython import TwythonStreamer

r = redis.StrictRedis(host='172.17.0.2', port=6379, password='letmeinplease', charset="utf-8", decode_responses=True)
r.setnx('pk',0)
r.setnx('keyword','unset')

TAPIKEY = ''
TAPISECRET = ''
TACCESSTOKEN = ''
TACCESSTOKENSECRET = ''

#TACCESSTOKEN2 = ''
#twitter = Twython(TAPIKEY, access_token=TACCESSTOKEN2)

class TDataStream(TwythonStreamer):
	def on_success(self, data):
		values = []
		#todo: increment pk and add values to database
		if 'text' in data:
			txt = data['text'].encode('utf-8')
			values.append('text:   ' + str(txt))
		if 'user' in data:
			location = data['user']['location']
			lang = data['user']['lang']
			values.append('loc:    ' + str(location))
			values.append('lang:   ' + str(lang))
		if 'coordinates' in data:
			cor = data['coordinates']
			values.append('coord:  ' + str(cor))
		if 'place' in data and data['place'] is not None:
			fullname = data['place']['full_name']
			country = data['place']['country']
			values.append('fname:  ' + str(fullname))
			values.append('cntry:  ' + str(country))
		
		for val in values:
			print(val)

		if keyword != r.get('keyword'):
			self.disconnect()

	def on_error(self, status_code, data):
		print(status_code)
		self.disconnect()

streamer = TDataStream(TAPIKEY, TAPISECRET, TACCESSTOKEN, TACCESSTOKENSECRET)

while True:
	keyword = r.get('keyword')
	if keyword is not None and keyword != 'unset':
		streamer.statuses.filter(track = keyword)
	else:
		time.sleep(0.5)
