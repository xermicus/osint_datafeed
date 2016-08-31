from twython import Twython
from twython import TwythonStreamer

TAPIKEY = ''
TAPISECRET = ''
TACCESSTOKEN = ''
TACCESSTOKENSECRET = ''

#TACCESSTOKEN2 = ''
#twitter = Twython(TAPIKEY, access_token=TACCESSTOKEN2)

class TDataStream(TwythonStreamer):
	def on_success(self, data):
		values = []
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

		def on_error(self, status_code, data):
			print(status_code)
			self.disconnect()

streamer = TDataStream(TAPIKEY, TAPISECRET, TACCESSTOKEN, TACCESSTOKENSECRET)
streamer.statuses.filter(track = 'foo');
