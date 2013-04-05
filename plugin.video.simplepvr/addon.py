import sys
import urllib
import urllib2
import urlparse
import base64
import simplejson

import xbmcaddon
import xbmcgui
import xbmcplugin

class SimplePvrException(Exception):
    pass

class SimplePvr(object):

    def showOverview(self):
        shows = self.get(BASE_URL + '/api/shows')

        for show in shows:
            item = xbmcgui.ListItem(show['name'])
            item.setInfo(type = 'video', infoLabels = {
                'title' : show['name'],
                'plot' : 'The plot'
            })
            item.addContextMenuItems([('Delete', 'XBMC.RunPlugin(' + PATH + '?' + self.urlencode({ 'operation': 'deleteShow', 'showId': show['id'] }) + ')',)])
            url = PATH + '?' + self.urlencode({ 'operation': 'showShow', 'showId': show['id'] })
            xbmcplugin.addDirectoryItem(HANDLE, url, item, True)

        xbmcplugin.endOfDirectory(HANDLE)

    def urlencode(self, dictionary):
        encoded_dictionary = {}
        for k, v in dictionary.iteritems():
            if isinstance(v, unicode):
                v = v.encode('utf8')
            elif isinstance(v, str):
                # Must be encoded in UTF-8
                v.decode('utf8')
            encoded_dictionary[k] = v
        return urllib.urlencode(encoded_dictionary)

    def showShow(self, showId):
        url = BASE_URL + '/api/shows/' + urllib2.quote(showId) + '/recordings'
        items = list()
        episodes = self.get(url)

        for episode in episodes:
            episodeNumber = episode['episode']
            item = xbmcgui.ListItem(episodeNumber)

            day = episode['start_time'][8:10]
            month = episode['start_time'][5:7]
            year = episode['start_time'][0:4]

            date = '%s.%s.%s' % (day, month, year)
            aired = '%s-%s-%s' % (year, month, day)

            infoLabels = {
                'title' : episode['show_id'],
                'plot' : episode['description'],
                'date' : date,
                'aired' : aired,
                #'duration' : episode['duration'],
            }
            item.setInfo('video', infoLabels)
            item.addContextMenuItems([('Delete', 'XBMC.RunPlugin(' + PATH + '?' + self.urlencode({ 'operation': 'deleteRecording', 'showId': showId, 'episodeNumber': episodeNumber }) + ')',)])
            items.append((episode['local_file_url'], item, False))

        xbmcplugin.addDirectoryItems(HANDLE, items)
        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.endOfDirectory(HANDLE)

    def deleteShow(self, showId):
        if xbmcgui.Dialog().yesno('OK to delete?', 'Really delete all episodes of', showId, '?'):
            url = BASE_URL + '/api/shows/' + urllib2.quote(showId)
            self.delete(url)
            xbmc.executebuiltin('XBMC.Container.Refresh()')

    def deleteRecording(self, showId, episodeNumber):
        if xbmcgui.Dialog().yesno('OK to delete?', 'Really delete episode ' + episodeNumber + ' of', showId, '?'):
            url = BASE_URL + '/api/shows/' + urllib2.quote(showId) + '/recordings/' + urllib2.quote(episodeNumber)
            self.delete(url)
            xbmc.executebuiltin('XBMC.Container.Refresh()')

    def showError(self, message = 'n/a'):
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)

        line1 = ADDON.getLocalizedString(30900)
        line2 = ADDON.getLocalizedString(30901)
        xbmcgui.Dialog().ok('Something went wrong...', message)

    def showMessage(self, message):
        xbmcgui.Dialog().ok('Message', 'Linje 1', 'Linje 2', message)

    def get(self, url):
        try:
            request = self.createRequest(url)
            url = urllib2.urlopen(request)
            response = url.read().decode('utf-8')
            url.close()
            return simplejson.loads(response)
        except Exception, ex:
            raise SimplePvrException(ex)

    def delete(self, url):
        try:
            request = self.createRequest(url)
            request.get_method = lambda: 'DELETE'
            url = urllib2.urlopen(request)
            url.close()
        except Exception, ex:
            raise SimplePvrException(ex)

    def createRequest(self, url):
        userName = ADDON.getSetting('backend.userName')
        password = ADDON.getSetting('backend.password')
        request = urllib2.Request(url)
        if userName != '':
            base64string = base64.encodestring('%s:%s' % (userName, password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
        return request


if __name__ == '__main__':
    ADDON = xbmcaddon.Addon()
    PATH = sys.argv[0]
    HANDLE = int(sys.argv[1])
    PARAMS = sys.argv[2]
    BASE_URL = ADDON.getSetting('backend.url')

    simplePvr = SimplePvr()
    try:
        if PARAMS != '':
            queryString = PARAMS[1:] # remove '?'
            parameters = urlparse.parse_qs(queryString)
            operation = parameters['operation'][0]

            if operation == 'showShow':
                showId = parameters['showId'][0]
                simplePvr.showShow(showId)
            elif operation == 'deleteShow':
                showId = parameters['showId'][0]
                simplePvr.deleteShow(showId)
            elif operation == 'deleteRecording':
                showId = parameters['showId'][0]
                episodeNumber = parameters['episodeNumber'][0]
                simplePvr.deleteRecording(showId, episodeNumber)
        else:
            simplePvr.showOverview()

    except SimplePvrException, ex:
        simplePvr.showError(str(ex))

    except Exception, ex:
        simplePvr.showError(str(ex))
