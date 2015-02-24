import sys
import urllib
import urlparse
import xbmcgui
import xbmcaddon
import xbmcplugin
import logging

from resources.lib import zing_api

addon = xbmcaddon.Addon()
my_setting = addon.getSetting('my_setting')
addon_name = addon.getAddonInfo('name')

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

#========================================================================
#=================== UI Functions =======================================
#========================================================================

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def show_genres(genres):
    for genre in genres:
        url = build_url({
            'mode': 'genre', 
            'genre_id': genre['id']
        })
        li = xbmcgui.ListItem('Genre - ' + genre['name'])
        xbmcplugin.addDirectoryItem(
            handle=addon_handle, url=url, listitem=li, isFolder=True)

def show_programs(programs):
    for program in programs:
        url = build_url({
            'mode': 'program', 
            'program_id': program['id']
        })
        li = xbmcgui.ListItem('Program - ' + program['name'])
        xbmcplugin.addDirectoryItem(
            handle=addon_handle, url=url, listitem=li, isFolder=True)

def show_series(series):
    for seri in series:
        url = build_url({
            'mode': 'seri', 
            'seri_id': seri['id'],
            'total': seri['total']
        })
        li = xbmcgui.ListItem('Series - ' + seri['name'])
        xbmcplugin.addDirectoryItem(
            handle=addon_handle, url=url, listitem=li, isFolder=True)

def show_medias(medias):
    for media in medias:
        # url = build_url({
        #     'mode': 'media', 
        #     'media_id': media['id'],
        #     'file_url': media['file_url']
        # })
        url = 'http://' + media['file_url']
        li = xbmcgui.ListItem('Media - ' + media['full_name'])
        xbmcplugin.addDirectoryItem(
            handle=addon_handle, url=url, listitem=li, isFolder=False)

#========================================================================
#=================== DISPATCHER =========================================
#========================================================================

def dispatch(mode):
    if mode is None:
        genres = zing_api.genre_child()['response']
        show_genres(genres)
        
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode[0] == 'genre':
        genre_id = args['genre_id'][0]

        # check if this's leaf genre or not
        # if not, show its children
        # else show program

        leaf_genre = False

        if 'page' in args:
            leaf_genre = True
            page = int(args['page'][0])
        else:
            # check by making request
            genres = zing_api.genre_child(genre_id)['response']
            if len(genres) > 0:
                show_genres(genres)
                leaf_genre = False
            else:
                leaf_genre = True
                page = 1
        
        if leaf_genre:
            res = zing_api.program_list(genre_id, page=page)
            
            programs = res['response']
            show_programs(programs)

            # add next page button
            next_page = res.get('next')
            if next_page is not None:
                url = build_url({
                    'mode': 'genre', 
                    'genre_id': genre_id,
                    'page': next_page
                })
                li = xbmcgui.ListItem('-> Page %s' % next_page)
                xbmcplugin.addDirectoryItem(
                    handle=addon_handle, url=url, listitem=li, isFolder=True)
            # add 1st page btn
            if page > 1:
                url = build_url({
                    'mode': 'genre', 
                    'genre_id': genre_id,
                    'page': 1
                })
                li = xbmcgui.ListItem('<-First Page')
                xbmcplugin.addDirectoryItem(
                    handle=addon_handle, url=url, listitem=li, isFolder=True)
        
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode[0] == 'program':
        # show series
        program_id = args['program_id'][0]
        resp = zing_api.program_info(program_id)
        if 'response' in resp:
            program_info = resp['response']
            series = program_info['series']
            # if len(series) == 1:
            #     seri_id = series[0]['id']
            #     medias = zing_api.series_medias(seri_id)['response']
            #     show_medias(medias)
            # else:
            #     show_series(series)
            show_series(series)
        else:
            msg = 'Code: %s - %s' % (resp.get('code'), resp.get('message'))
            xbmcgui.Dialog().ok(addon_name, msg)
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode[0] == 'seri':
        # show medias
        seri_id = args['seri_id'][0]
        count = 10
        if 'page' in args:
            page = int(args['page'][0])
        else:
            total = int(args['total'][0])
            page = (total / count) + 1
            print('First page: %s' % page)
        
        medias = zing_api.series_medias(seri_id, count=count, page=page)['response']
        show_medias(reversed(medias))

        # add next page button
        next_page = page - 1
        if next_page > 0:
            url = build_url({
                'mode': 'seri', 
                'seri_id': seri_id,
                'page': next_page
            })
            li = xbmcgui.ListItem('-> Page %s' % next_page)
            xbmcplugin.addDirectoryItem(
                handle=addon_handle, url=url, listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(addon_handle)

    elif mode[0] == 'media':
        # play media
        media_id = args['media_id'][0]
        file_url = args['file_url'][0]

        url = 'http://google.com'
        li = xbmcgui.ListItem(foldername + ' Video', iconImage='DefaultVideo.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        xbmcplugin.endOfDirectory(addon_handle)

# RUN
mode = args.get('mode', None)
dispatch(mode)
