import re
import urllib
import urllib2

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

    def video_url(self, show, episode):
        if self.user_name != '':
            matches = re.search('(https?://)(.*[^/])/?', self.base_url)
            base = matches.group(1) + self.user_name + ':' + self.password + '@' + matches.group(2)
        else:
            base = self.base_url
        return base + '/api/shows/' + urllib2.quote(show) + '/recordings/' + episode + '/stream.ts'
