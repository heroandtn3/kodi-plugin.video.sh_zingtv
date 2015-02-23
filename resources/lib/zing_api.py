# -*- coding: utf-8 -*-
import requests
import json

API_ENPOINT = 'http://api.tv.zing.vn/3.0/'
API_KEY='d04210a70026ad9323076716781c223f'
SESSION_KEY = '91618dfec493ed7dc9d61ac088dff36b'

def genre_child(genre_id=None):
    """
    Return all genre's children of specify genre.

    If genre_id is not specified, this will return root genres.
    """
    url = API_ENPOINT + 'genre/child'
    if genre_id is not None:
        return requests.get(url, params={
            'api_key': API_KEY,
            'session_key': SESSION_KEY,
            'genre_id': genre_id
        }).json()
    else:
        return {
            'total': 1,
            'response': [{
                'id': 78,
                'name': 'TV Show'
            }, {
                'id': 82,
                'name': 'Phim truyền hình'
            }, {
                'id': 83,
                'name': 'Hoạt hình'
            }, {
                'id': 86,
                'name': 'Hài hước'
            }, {
                'id': 168,
                'name': 'Thiếu nhi'
            }, {
                'id': 87,
                'name': 'Khoa học - Giáo dục'
            }, {
                'id': 92,
                'name': 'Âm nhạc'
            },]
        }

def program_list(genre_id, count=10, page=1):
    """
    Get list of programs within genre.
    This will add `next` filed to specify next page. If it's the last page,
    no `next` field is added.
    """
    url = API_ENPOINT + 'program/list'
    res = requests.get(url, params={
            'api_key': API_KEY,
            'session_key': SESSION_KEY,
            'genre_id': genre_id,
            'count': count,
            'page': page
        }).json()

    # check if there is next page
    if len(res['response']) == count:
        res['next'] = page + 1
    return res

def program_info(program_id):
    """
    Return detail information of a program.
    """
    url = API_ENPOINT + 'program/info'
    res = requests.get(url, params={
            'api_key': API_KEY,
            'session_key': SESSION_KEY,
            'program_id': program_id
        }).json()
    return res

def series_medias(series_id, count=10, page=1):
    """
    Return all medias (episodes) within series.
    """
    url = API_ENPOINT + 'series/medias'
    res = requests.get(url, params={
            'api_key': API_KEY,
            'session_key': SESSION_KEY,
            'series_id': series_id,
            'count': count,
            'page': page
        }).json()
    return res