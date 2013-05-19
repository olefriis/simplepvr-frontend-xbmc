import re
import urllib
import urllib2
import simplejson
import operator

class SimplePvrException(Exception):
    pass

class SimplePvrNoConnectionToHostException(SimplePvrException):
    pass

class SimplePvrAuthenticationException(SimplePvrException):
    pass

class SimplePvrClient(object):
    def __init__(self, base_url, user_name, password, same_machine=False):
        base_url_matches = re.search('(https?://)(.*[^/])/?', base_url)
        self.base_url = base_url_matches.group(1) + base_url_matches.group(2)
        self.user_name = user_name
        self.password = password
        self.same_machine = same_machine

    def authenticate(self):
        if self.user_name != '':
            password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_manager.add_password(None, self.base_url, self.user_name, self.password)
            handler = urllib2.HTTPBasicAuthHandler(password_manager)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)

    def shows(self):
        shows_json = self.get_json(self.base_url + '/api/shows')

        result = []
        for show_json in shows_json:
            result.append(SimplePvrShow(show_json['id'], show_json['name']))
        result.sort(key=operator.attrgetter('name'))

        return result

    def recordings_of_show(self, show_id):
        recordings_json = self.get_json(self.base_url + '/api/shows/' + urllib2.quote(show_id) + '/recordings')

        result = []
        for recording_json in recordings_json:
            if self.same_machine:
                url = recording_json['local_file_url']
            else:
                url = self.path_to_recording(show_id, recording_json['id'])
            result.append(SimplePvrRecording(recording_json['show_id'], recording_json['episode'], recording_json['subtitle'],
                recording_json['description'], recording_json['start_time'], url))

        return result

    def delete_show(self, show_id):
        url = self.base_url + '/api/shows/' + urllib2.quote(show_id)
        self.delete(url)

    def delete_recording_of_show(self, show_id, episode_number):
        url = self.base_url + '/api/shows/' + urllib2.quote(show_id) + '/recordings/' + urllib2.quote(episode_number)
        self.delete(url)

    def path_to_recording(self, show, episode):
        if self.user_name != '':
            matches = re.search('(https?://)(.*[^/])', self.base_url)
            base = matches.group(1) + self.user_name + ':' + self.password + '@' + matches.group(2)
        else:
            base = self.base_url
        return base + '/api/shows/' + urllib2.quote(show) + '/recordings/' + episode + '/stream.ts'

    def get_json(self, url):
        return simplejson.loads(self.get(url))

    def get(self, url):
        request = self.create_request(url)
        try:
            url = urllib2.urlopen(request)
        except urllib2.HTTPError, ex:
            if ex.code == 401:
                raise SimplePvrAuthenticationException(ex)
            else:
                raise SimplePvrNoConnectionToHostException(ex)
        except urllib2.URLError, ex:
            raise SimplePvrNoConnectionToHostException(ex)
        response = url.read().decode('utf-8')
        url.close()
        return response

    def delete(self, url):
        try:
            request = self.create_request(url)
            request.get_method = lambda: 'DELETE'
            url = urllib2.urlopen(request)
            url.close()
        except Exception, ex:
            raise SimplePvrException(ex)

    def create_request(self, url):
        return urllib2.Request(url)

class SimplePvrShow(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

class SimplePvrRecording(object):
    def __init__(self, show_id, episode, subtitle, description, start_time, url):
        self.show_id = show_id
        self.episode = episode
        self.subtitle = subtitle
        self.description = description
        self.start_time = start_time
        self.url = url
