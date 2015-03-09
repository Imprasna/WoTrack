import json
import requests
from spotify.utils.cache import Cache


class SpotifyClient(object):
    def format_track_response(self, response_data):
        """
        :param response_data: dictionary formatted response data received from Spotify
        :return tracks : (list) formatted track data with the name, artist, image, and track url.
        """
        tracks = []
        for track in response_data['tracks']['items']:
            track_image = 'n/a/'
            if track.get('album').get('images'):
                track_image = track['album']['images'][0]

            track_artist = 'n/a'
            if track.get('artists'):
                track_artist = track['artists'][0]['name']

            tracks.append({
                'name': track.get('name').lower(),
                'artist': track_artist,
                'image': track_image,
                'url': track.get('external_urls')['spotify'],
            })
        return tracks

    def get_tracks(self, query):
        """
        :param query: search query to use
        :return tracks: (list) retrieved from Spotify
        """
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

            tracks = self.format_track_response(response_data)

            Cache.set(query, tracks)
            return tracks

    _limit = 25