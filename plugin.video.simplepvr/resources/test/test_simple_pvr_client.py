import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib/'))
from simple_pvr_client import SimplePvrClient

class TestSimplePvrClient:
	def test_can_get_empty_list_of_shows(self):
		client = SimplePvrClient('http://my-site.com:4567', '', '')
		client.get = self.fake_get
		self.expected_url = 'http://my-site.com:4567/api/shows'
		self.get_response = '[]'

		shows = client.shows()
		assert len(shows) == 0

	def test_can_get_list_of_shows(self):
		client = SimplePvrClient('http://my-site.com:4567', '', '')
		client.get = self.fake_get
		self.expected_url = 'http://my-site.com:4567/api/shows'
		self.get_response = '[{"id":"Klovn - The Movie","name":"Klovn - The Movie"},{"id":"Blachman","name":"Blachman"},{"id":"The Man Who Wasnt There","name":"The Man Who Wasnt There"}]'

		shows = client.shows()
		assert len(shows) == 3
		assert shows[0].id == 'Blachman'
		assert shows[0].name == 'Blachman'
		assert shows[1].id == 'Klovn - The Movie'
		assert shows[1].name == 'Klovn - The Movie'
		assert shows[2].id == 'The Man Who Wasnt There'
		assert shows[2].name == 'The Man Who Wasnt There'

	def test_can_get_information_on_recordings(self):
		client = SimplePvrClient('http://my-site.com:4567', '', '')
		client.get = self.fake_get
		self.expected_url = 'http://my-site.com:4567/api/shows/The%20Man%20Who%20Wasnt%20There/recordings'
		self.get_response = """[
			{"id":"1","show_id":"The Man Who Wasnt There","episode":"1","subtitle":"Amerikansk krimidrama fra 2001.","description":"Ed passer sin daglige dont i fris\u00f8rsalonen i 1949, hvor der stadig var sort-hvide film og livsfarlige blondiner. Da en skaldet handelsrejsende kommer forbi med en fidus, ser Ed sit livs chance. Han afpresser Big Dave, som hans kone Doris har en aff\u00e6re med. Planen ser skudsikker ud, men det eneste, der er sikkert, er, at nogen bliver skudt. Og nogen ender i stolen for mord.","start_time":"2013-04-20T21:28:00+02:00","channel_name":"DR K","has_thumbnail":false,"has_webm":false,"local_file_url":"file:///data/simplePVR/simplepvr/recordings/The Man Who Wasnt There/1/stream.ts"},
			{"id":"2","show_id":"The Man Who Was There","episode":"2","subtitle":"Oh well...","description":"Just a 2nd recording for test purposes...","start_time":"2013-04-25T05:35:00+02:00","channel_name":"DR 1","has_thumbnail":false,"has_webm":false,"local_file_url":"file:///data/simplePVR/simplepvr/recordings/The Man Who Was There/2/stream.ts"}
			]"""

		recordings = client.recordings_of_show('The Man Who Wasnt There')
		assert len(recordings) == 2
		assert recordings[0].show_id == 'The Man Who Wasnt There'
		assert recordings[0].episode == '1'
		assert recordings[0].subtitle == 'Amerikansk krimidrama fra 2001.'
		assert recordings[0].description.startswith(u"Ed passer sin daglige dont i fris\xf8rsalonen i 1949")
		assert recordings[0].start_time == '2013-04-20T21:28:00+02:00'

	def test_gives_local_file_url_for_recordings_when_on_same_machine(self):
		client = SimplePvrClient('http://my-site.com:4567', '', '', same_machine=True)
		client.get = self.fake_get
		self.expected_url = 'http://my-site.com:4567/api/shows/The%20Man%20Who%20Wasnt%20There/recordings'
		self.get_response = """[
			{"id":"1","show_id":"The Man Who Wasnt There","episode":"1","subtitle":"Amerikansk krimidrama fra 2001.","description":"Ed passer sin daglige dont i fris\u00f8rsalonen i 1949, hvor der stadig var sort-hvide film og livsfarlige blondiner. Da en skaldet handelsrejsende kommer forbi med en fidus, ser Ed sit livs chance. Han afpresser Big Dave, som hans kone Doris har en aff\u00e6re med. Planen ser skudsikker ud, men det eneste, der er sikkert, er, at nogen bliver skudt. Og nogen ender i stolen for mord.","start_time":"2013-04-20T21:28:00+02:00","channel_name":"DR K","has_thumbnail":false,"has_webm":false,"local_file_url":"file:///data/simplePVR/simplepvr/recordings/The Man Who Wasnt There/1/stream.ts"}
			]"""

		recordings = client.recordings_of_show('The Man Who Wasnt There')
		assert recordings[0].url == 'file:///data/simplePVR/simplepvr/recordings/The Man Who Wasnt There/1/stream.ts'

	def test_can_construct_simple_video_url_when_no_authentication_and_no_port_number(self):
		client = SimplePvrClient('http://hello.co.uk', '', '', same_machine=False)
		client.get = self.fake_get
		self.expected_url = 'http://hello.co.uk/api/shows/The%20Man%20Who%20Wasnt%20There/recordings'
		self.get_response = """[
			{"id":"4","show_id":"The Man Who Wasnt There","episode":"1","subtitle":"Amerikansk krimidrama fra 2001.","description":"Ed passer sin daglige dont i fris\u00f8rsalonen i 1949, hvor der stadig var sort-hvide film og livsfarlige blondiner. Da en skaldet handelsrejsende kommer forbi med en fidus, ser Ed sit livs chance. Han afpresser Big Dave, som hans kone Doris har en aff\u00e6re med. Planen ser skudsikker ud, men det eneste, der er sikkert, er, at nogen bliver skudt. Og nogen ender i stolen for mord.","start_time":"2013-04-20T21:28:00+02:00","channel_name":"DR K","has_thumbnail":false,"has_webm":false,"local_file_url":"file:///data/simplePVR/simplepvr/recordings/The Man Who Wasnt There/1/stream.ts"}
			]"""

		recordings = client.recordings_of_show('The Man Who Wasnt There')
		assert recordings[0].url == 'http://hello.co.uk/api/shows/The%20Man%20Who%20Wasnt%20There/recordings/4/stream.ts'

	def test_can_construct_simple_video_url_when_no_authentication(self):
		client = SimplePvrClient('http://hello.co.uk:4567', '', '', same_machine=False)
		client.get = self.fake_get
		self.expected_url = 'http://hello.co.uk:4567/api/shows/The%20Man%20Who%20Wasnt%20There/recordings'
		self.get_response = """[
			{"id":"4","show_id":"The Man Who Wasnt There","episode":"1","subtitle":"Amerikansk krimidrama fra 2001.","description":"Ed passer sin daglige dont i fris\u00f8rsalonen i 1949, hvor der stadig var sort-hvide film og livsfarlige blondiner. Da en skaldet handelsrejsende kommer forbi med en fidus, ser Ed sit livs chance. Han afpresser Big Dave, som hans kone Doris har en aff\u00e6re med. Planen ser skudsikker ud, men det eneste, der er sikkert, er, at nogen bliver skudt. Og nogen ender i stolen for mord.","start_time":"2013-04-20T21:28:00+02:00","channel_name":"DR K","has_thumbnail":false,"has_webm":false,"local_file_url":"file:///data/simplePVR/simplepvr/recordings/The Man Who Wasnt There/1/stream.ts"}
			]"""

		recordings = client.recordings_of_show('The Man Who Wasnt There')
		assert recordings[0].url == 'http://hello.co.uk:4567/api/shows/The%20Man%20Who%20Wasnt%20There/recordings/4/stream.ts'

	def test_can_construct_video_url_with_username_and_password(self):
		client = SimplePvrClient('http://my-site.com:4567', 'Me', 'Secret', same_machine=False)
		client.get = self.fake_get
		self.expected_url = 'http://my-site.com:4567/api/shows/The%20Man%20Who%20Wasnt%20There/recordings'
		self.get_response = """[
			{"id":"4","show_id":"The Man Who Wasnt There","episode":"1","subtitle":"Amerikansk krimidrama fra 2001.","description":"Ed passer sin daglige dont i fris\u00f8rsalonen i 1949, hvor der stadig var sort-hvide film og livsfarlige blondiner. Da en skaldet handelsrejsende kommer forbi med en fidus, ser Ed sit livs chance. Han afpresser Big Dave, som hans kone Doris har en aff\u00e6re med. Planen ser skudsikker ud, men det eneste, der er sikkert, er, at nogen bliver skudt. Og nogen ender i stolen for mord.","start_time":"2013-04-20T21:28:00+02:00","channel_name":"DR K","has_thumbnail":false,"has_webm":false,"local_file_url":"file:///data/simplePVR/simplepvr/recordings/The Man Who Wasnt There/1/stream.ts"}
			]"""

		recordings = client.recordings_of_show('The Man Who Wasnt There')
		assert recordings[0].url == 'http://Me:Secret@my-site.com:4567/api/shows/The%20Man%20Who%20Wasnt%20There/recordings/4/stream.ts'

	def test_handles_ending_slash_in_base_url_when_creating_video_url(self):
		client = SimplePvrClient('http://my-site.com:4567/', 'Me', 'Secret', same_machine=False)
		client.get = self.fake_get
		self.expected_url = 'http://my-site.com:4567/api/shows/The%20Man%20Who%20Wasnt%20There/recordings'
		self.get_response = """[
			{"id":"4","show_id":"The Man Who Wasnt There","episode":"1","subtitle":"Amerikansk krimidrama fra 2001.","description":"Ed passer sin daglige dont i fris\u00f8rsalonen i 1949, hvor der stadig var sort-hvide film og livsfarlige blondiner. Da en skaldet handelsrejsende kommer forbi med en fidus, ser Ed sit livs chance. Han afpresser Big Dave, som hans kone Doris har en aff\u00e6re med. Planen ser skudsikker ud, men det eneste, der er sikkert, er, at nogen bliver skudt. Og nogen ender i stolen for mord.","start_time":"2013-04-20T21:28:00+02:00","channel_name":"DR K","has_thumbnail":false,"has_webm":false,"local_file_url":"file:///data/simplePVR/simplepvr/recordings/The Man Who Wasnt There/1/stream.ts"}
			]"""

		recordings = client.recordings_of_show('The Man Who Wasnt There')
		assert recordings[0].url == 'http://Me:Secret@my-site.com:4567/api/shows/The%20Man%20Who%20Wasnt%20There/recordings/4/stream.ts'

	def fake_get(self, url):
		sys.stdout.write('URL: ' + url)
		assert url == self.expected_url
		return self.get_response