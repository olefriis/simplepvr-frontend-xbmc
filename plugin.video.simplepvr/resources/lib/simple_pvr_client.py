import re
import urllib
import urllib2
import simplejson

class SimplePvrException(Exception):
    pass

class SimplePvrClient(object):
    def __init__(self, base_url, user_name, password):
        self.base_url = base_url
        self.user_name = user_name
        self.password = password

    def authenticate(self):
        if self.user_name != '':
            password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_manager.add_password(None, self.base_url, self.user_name, self.password)
            handler = urllib2.HTTPBasicAuthHandler(password_manager)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)

    def shows(self):
        return self.get(self.base_url + '/api/shows')

    def recordings_of_show(self, show_id):
        url = self.base_url + '/api/shows/' + urllib2.quote(show_id) + '/recordings'
        return self.get(url)

    def delete_show(self, show_id):
        url = self.base_url + '/api/shows/' + urllib2.quote(show_id)
        self.delete(url)

    def delete_recording_of_show(self, show_id, episode_number):
        url = self.base_url + '/api/shows/' + urllib2.quote(show_id) + '/recordings/' + urllib2.quote(episode_number)
        self.delete(url)


    def video_url(self, show, episode):
        if self.user_name != '':
            matches = re.search('(https?://)(.*[^/])/?', self.base_url)
            base = matches.group(1) + self.user_name + ':' + self.password + '@' + matches.group(2)
        else:
            base = self.base_url
        return base + '/api/shows/' + urllib2.quote(show) + '/recordings/' + episode + '/stream.ts'

    def get(self, url):
        try:
            request = self.create_request(url)
            url = urllib2.urlopen(request)
            response = url.read().decode('utf-8')
            url.close()
            return simplejson.loads(response)
        except Exception, ex:
            raise SimplePvrException(ex)

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
