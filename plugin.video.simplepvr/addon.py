import sys
import os
import urllib
import urllib2
import urlparse

import xbmcaddon
import xbmcgui
import xbmcplugin

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources/lib/'))
from simple_pvr_client import SimplePvrClient, SimplePvrException

class SimplePvr(object):
    def __init__(self, client):
        self.client = client

    def show_overview(self):
        for show in client.shows():
            item = xbmcgui.ListItem(show.name)
            item.setInfo(type = 'video', infoLabels = {
                'title' : show.name
            })
            item.addContextMenuItems([('Delete', 'XBMC.RunPlugin(' + PATH + '?' + self.url_encode({ 'operation': 'delete_show', 'show_id': show.id }) + ')',)])
            url = PATH + '?' + self.url_encode({ 'operation': 'show_show', 'show_id': show.id })
            xbmcplugin.addDirectoryItem(HANDLE, url, item, True)

        xbmcplugin.endOfDirectory(HANDLE)

    def show_show(self, show_id):
        items = list()

        for recording in client.recordings_of_show(show_id):
            item = xbmcgui.ListItem(recording.episode)

            day = recording.start_time[8:10]
            month = recording.start_time[5:7]
            year = recording.start_time[0:4]

            date = '%s.%s.%s' % (day, month, year)
            aired = '%s-%s-%s' % (year, month, day)

            infoLabels = {
                'title' : recording.show_id,
                'plot' : recording.description,
                'date' : date,
                'aired' : aired,
                #'duration' : recording.duration,
            }
            item.setInfo('video', infoLabels)
            item.addContextMenuItems([('Delete', 'XBMC.RunPlugin(' + PATH + '?' + self.url_encode({ 'operation': 'delete_recording', 'show_id': recording.show_id, 'episode_number': recording.episode }) + ')',)])

            if SAME_MACHINE == 'true':
                items.append((recording.local_file_url, item, False))
            else:
                items.append((client.video_url(show_id, recording.episode), item, False))

        xbmcplugin.addDirectoryItems(HANDLE, items)
        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.endOfDirectory(HANDLE)

    def delete_show(self, show_id):
        if xbmcgui.Dialog().yesno('OK to delete?', 'Really delete all episodes of', show_id, '?'):
            client.delete_show(show_id)
            xbmc.executebuiltin('XBMC.Container.Refresh()')

    def delete_recording(self, show_id, episode_number):
        if xbmcgui.Dialog().yesno('OK to delete?', 'Really delete episode ' + episode_number + ' of', show_id, '?'):
            client.delete_recording_of_show(show_id, episode_number)
            xbmc.executebuiltin('XBMC.Container.Refresh()')

    def show_error(self, message = 'n/a'):
        sys.stdout.write(message)
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
        xbmcgui.Dialog().ok('Something went wrong...', message)

    def show_message(self, message):
        xbmcgui.Dialog().ok('Message', 'Linje 1', 'Linje 2', message)

    def url_encode(self, dictionary):
        encoded_dictionary = {}
        for k, v in dictionary.iteritems():
            if isinstance(v, unicode):
                v = v.encode('utf8')
            elif isinstance(v, str):
                # Must be encoded in UTF-8
                v.decode('utf8')
            encoded_dictionary[k] = v
        return urllib.urlencode(encoded_dictionary)

if __name__ == '__main__':
    ADDON = xbmcaddon.Addon()
    PATH = sys.argv[0]
    HANDLE = int(sys.argv[1])
    PARAMS = sys.argv[2]
    SAME_MACHINE = ADDON.getSetting('backend.sameMachine')
    base_url = ADDON.getSetting('backend.url')
    user_name = ADDON.getSetting('backend.userName')
    password = ADDON.getSetting('backend.password')

    client = SimplePvrClient(base_url, user_name, password)
    client.authenticate()

    simple_pvr = SimplePvr(client)
    try:
        if PARAMS != '':
            queryString = PARAMS[1:] # remove '?'
            parameters = urlparse.parse_qs(queryString)
            operation = parameters['operation'][0]

            if operation == 'show_show':
                show_id = parameters['show_id'][0]
                simple_pvr.show_show(show_id)
            elif operation == 'delete_show':
                show_id = parameters['show_id'][0]
                simple_pvr.delete_show(show_id)
            elif operation == 'delete_recording':
                show_id = parameters['show_id'][0]
                episode_number = parameters['episode_number'][0]
                simple_pvr.delete_recording(show_id, episode_number)
        else:
            simple_pvr.show_overview()

    except SimplePvrException, ex:
        simple_pvr.show_error(str(ex))

    except Exception, ex:
        simple_pvr.show_error(str(ex))
