import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib/'))
from simple_pvr_client import SimplePvrClient

class TestSimplePvrClient:
	def test_can_construct_simple_video_url_when_no_authentication_and_no_port_number(self):
		client = SimplePvrClient('http://hello.co.uk', '', '')
		assert client.video_url('New Show', '4') == 'http://hello.co.uk/api/shows/New%20Show/recordings/4/stream.ts'

	def test_can_construct_simple_video_url_when_no_authentication(self):
		client = SimplePvrClient('http://hello.co.uk:4567', '', '')
		assert client.video_url('New Show', '4') == 'http://hello.co.uk:4567/api/shows/New%20Show/recordings/4/stream.ts'

	def test_can_construct_video_url_with_username_and_password(self):
		client = SimplePvrClient('http://my-site.com:4567', 'Me', 'Secret')
		assert client.video_url('Show', '23') == 'http://Me:Secret@my-site.com:4567/api/shows/Show/recordings/23/stream.ts'

	def test_handles_ending_slash_in_base_url_when_creating_video_url(self):
		client = SimplePvrClient('http://my-site.com:4567/', 'Me', 'Secret')
		assert client.video_url('Show', '23') == 'http://Me:Secret@my-site.com:4567/api/shows/Show/recordings/23/stream.ts'

	def test_can_get_list_of_shows(self):
		client = SimplePvrClient('http://my-site.com:4567', '', '')
		client.get = self.fake_get
		self.expected_url = 'http://my-site.com:4567/api/shows'
		self.get_response = '[{"id":"Klovn - The Movie","name":"Klovn - The Movie"},{"id":"Blachman","name":"Blachman"},{"id":"The Man Who Wasnt There","name":"The Man Who Wasnt There"}]'

		shows = client.shows()
		assert len(shows) == 3
		assert shows[0].id == 'Blachman'
		assert shows[0].name == 'Blachman'

	def fake_get(self, url):
		sys.stdout.write('URL: ' + url)
		assert url == self.expected_url
		return self.get_response