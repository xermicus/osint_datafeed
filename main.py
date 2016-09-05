import redis, time
from twython import Twython
from twython import TwythonStreamer

# Getting the databse ready
r = redis.StrictRedis(host='172.17.0.2', port=6379, password='letmeinplease', charset="utf-8", decode_responses=True)
r.setnx('pk',0)

# Getting Twitter API ready
TAPIKEY = ''
TAPIKEYSECRET = ''
TACCESSTOKEN = ''
TACCESSTOKENSECRET = ''
twitter = Twython(TAPIKEY, TAPIKEYSECRET, oauth_version=2)
ACCESSTOKEN = twitter.obtain_access_token()
twitter = Twython(TAPIKEY, access_token=ACCESSTOKEN)

def addrecord(text, location, lang):
	r.incr('pk')
	pk = str(r.get('pk'))
	r.hmset(pk, {'text':text, 'class':'new', 'location':location, 'score':0, 'lang':lang})
	r.sadd('new', pk)

class TDataStream(TwythonStreamer):
	def on_success(self, data):
		if 'text' in data:
			txt = str(data['text'].encode('utf-8'))
			if 'user' in data:
				location = str(data['user']['location'])
				lang = str(data['user']['lang'])
				if 'place' in data and data['place'] is not None:
					fullname = str(data['place']['full_name'])
					country = str(data['place']['country'])
					addrecord(txt, fullname, lang)

		if 'coordinates' in data:
			cor = data['coordinates']
		
		if keyword != str(r.get('keyword')):
			self.disconnect()


	def on_error(self, status_code, data):
		print(status_code)
		self.disconnect()


streamer = TDataStream(TAPIKEY, TAPIKEYSECRET, TACCESSTOKEN, TACCESSTOKENSECRET)

while True:
	keyword = str(r.get('keyword'))
	if keyword is not None and keyword != 'unset':
		streamer.statuses.filter(track=keyword)
		print('sleeping 60 seconds to avoid getting rate limited')
		time.sleep(60)
	else:
		print('keyword is not set.. retrying in a second')
		time.sleep(1)
