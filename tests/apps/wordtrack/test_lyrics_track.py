from hamcrest import assert_that, empty, not_
from apps.wordtrack.lyrics_track import LyricsTrack
from spotify.tests.integration import IntegrationTestCase


class TestLyricsTrack(IntegrationTestCase):
    def test_get_greatest_pmi_collocation_ngrams(self):
        lyrics_track = LyricsTrack(
            "The red ball was smooth and shiny. "
            "The green ball was bald and beautiful "
        )

        assert_that(lyrics_track.get_tracks(), empty())
        lyrics_track.process(ngram_degree=3)

        assert_that(lyrics_track.get_tracks(), not_(empty()))
