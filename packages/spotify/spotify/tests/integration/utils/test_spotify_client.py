from hamcrest import assert_that, equal_to, not_none, has_entries, contains, contains_inanyorder
from packages.spotify.spotify.utils.spotify_client import SpotifyClient
from spotify.tests.integration import IntegrationTestCase
from spotify.utils.cache import Cache


class TestSpotifyClient(IntegrationTestCase):
    def __init__(self):
        self.spotify_client = SpotifyClient()

    def test_get_tracks_for_common_term_returns_25_items(self):
        tracks = self.spotify_client.get_tracks(query='red')
        assert_that(len(tracks), equal_to(25))

    def test_get_tracks_caches_results_for_later_use(self):
        tracks = self.spotify_client.get_tracks(query='blue')
        assert_that(len(tracks), equal_to(25))

        cached_response = Cache.get('blue')
        assert_that(cached_response, not_none())