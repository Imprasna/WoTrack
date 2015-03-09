import string
import nltk
from nltk.collocations import *
from nltk.tokenize import word_tokenize
from apps.wordtrack.levenshtein_reduce import LevenshteinReduce
from spotify.utils.spotify_client import SpotifyClient


class LyricsTrack(object):
    def __init__(self, lyrics):
        """
        Converts the input lyrics to Spotify tracks
        :param lyrics: (str) lyrics
        """
        self.lyrics = lyrics.lower()
        self.original_lyrics = self.lyrics
        self.spotify_client = SpotifyClient()
        self.last_ngrams = []
        self.acceptable_levenshtein = 3
        self.acquired_tracks = []
        self.ngram_degree = 3

    def get_tracks_for_ngram(self, ngrams):
        """
        Makes a search request to Spotify using the
        terms of the ngrams as the search query
        :param ngrams: (list) ngrams
        :param tracks: (list) spotify tracks
        """
        return [
            {
                'phrase': ngram,
                'tracks': self.spotify_client.get_tracks(ngram),
            } for ngram in ngrams
        ]

    def convert_phrase_to_track(self, ngram_tracks, lyrics):
        """
        Given the tracks retrieved from Spotify for each ngram,
        a Levenshtein Reduce mapping is applied to the tracks
        and phrases from the input lyrics.
        :param ngram_tracks: (list) ngram_tracks
        :param lyrics: (str) lyrics
        :return lyrics: (str) consumed phrases are removed from lyrics
        """
        phrase_to_tracks = []
        for ngram_track in ngram_tracks:
            phrase_to_tracks.append(LevenshteinReduce(
                phrase=ngram_track['phrase'],
                tracks=ngram_track['tracks']
            ).get_most_similar_track())

        for track in phrase_to_tracks:
            if track and track['levenshtein'] <= self.acceptable_levenshtein:
                self.acquired_tracks.append(track)
                lyrics = lyrics.replace(track['phrase'], '').strip()
        return lyrics

    def process(self, ngram_degree=3):
        """
        Processes the lyrics into Spotify tracks. The lyrics is processed recursively
        :param ngram_degree: (int) the greatest degree of ngrams to use.
        """
        self.ngram_degree = ngram_degree

        self._remove_punctuations()

        if ngram_degree == 3:
            ngrams = self._get_trigrams_with_collocation_pmi_for_lyrics()
        elif ngram_degree == 2:
            ngrams = self._get_bigrams_with_collocation_pmi_for_lyrics()
        else:
            ngrams = self.lyrics.split(' ')

        self.last_ngrams = ngrams

        ngram_tracks = self.get_tracks_for_ngram(ngrams)

        self.lyrics = self.convert_phrase_to_track(ngram_tracks, self.lyrics)

        if self.lyrics.strip() != '':
            if len(self.last_ngrams) == len(ngrams):
                self.acceptable_levenshtein += 1

            self.ngram_degree -= 1
            self.process(self.ngram_degree)

    def get_tracks(self):
        """
        :return tracks: (list) the tracks best matching the lyrics.
        """
        return self.acquired_tracks

    def _get_bigrams_with_collocation_pmi_for_lyrics(self):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(word_tokenize(self.lyrics))
        bi_phraseme = finder.score_ngrams(bigram_measures.pmi)
        phrasemes = ["%s %s" % (phrase[0][0], phrase[0][1]) for phrase in bi_phraseme]
        return phrasemes

    def _get_trigrams_with_collocation_pmi_for_lyrics(self):
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        finder = TrigramCollocationFinder.from_words(word_tokenize(self.lyrics))
        tri_phraseme = finder.score_ngrams(trigram_measures.pmi)
        phrasemes = ["%s %s %s" % (phrase[0][0], phrase[0][1], phrase[0][2]) for phrase in tri_phraseme]
        return phrasemes

    def _remove_punctuations(self):
        for c in string.punctuation:
            self.lyrics = self.lyrics.replace(c, '')
