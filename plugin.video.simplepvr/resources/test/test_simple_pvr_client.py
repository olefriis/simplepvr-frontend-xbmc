import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib/'))
from simple_pvr_client import SimplePvrClient

def test_can_construct_simple_video_url_when_no_authentication_and_no_port_number():
	client = SimplePvrClient('http://hello.co.uk', '', '')
	assert client.video_url('New Show', '4') == 'http://hello.co.uk/api/shows/New%20Show/recordings/4/stream.ts'

def test_can_construct_simple_video_url_when_no_authentication():
	client = SimplePvrClient('http://hello.co.uk:4567', '', '')
	assert client.video_url('New Show', '4') == 'http://hello.co.uk:4567/api/shows/New%20Show/recordings/4/stream.ts'

def test_can_construct_video_url_with_username_and_password():
	client = SimplePvrClient('http://my-site.com:4567', 'Me', 'Secret')
	assert client.video_url('Show', '23') == 'http://Me:Secret@my-site.com:4567/api/shows/Show/recordings/23/stream.ts'

def test_handles_ending_slash_in_base_url_when_creating_video_url():
	client = SimplePvrClient('http://my-site.com:4567/', 'Me', 'Secret')
	assert client.video_url('Show', '23') == 'http://Me:Secret@my-site.com:4567/api/shows/Show/recordings/23/stream.ts'
