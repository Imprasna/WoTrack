import json
import requests
from spotify.utils.cache import Cache


class SpotifyGetResponse(Exception):
    def __init__(self, request):
        self._status_code = request.status_code
        self._data = {}

        if self._status_code == 200:
            self._data = json.loads(request.content)

    @property
    def status_code(self):
        return self._status_code

    @property
    def data(self):
        return self._data


class SpotifyClient(object):
    def get_tracks(self, query, strict=None):
        cached_data = Cache.get(query)

        if cached_data:
            return cached_data

        url = 'https://api.spotify.com/v1/search'
        payload = {
            'type': 'track',
            'limit': self._limit,
            'q': query,
        }

        request = requests.get(
            url=url,
            params=payload,
        )

        if request.status_code == 200:
            response_data = json.loads(request.content)

            tracks = []
            for track in response_data['tracks']['items']:
                track_image = 'n/a/'
                if track.get('album').get('images'):
                    track_image = track['album']['images'][0]

                track_artist= 'n/a'
                if track.get('artists'):
                    track_artist = track['artists'][0]['name']

                tracks.append({
                    'name': track.get('name').lower(),
                    'artist': track_artist,
                    'image': track_image,
                    'url': track.get('external_urls')['spotify'],
                })

            Cache.set(query, tracks)
            return tracks

    _limit = 25