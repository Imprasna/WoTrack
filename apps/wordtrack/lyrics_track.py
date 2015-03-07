import string
import nltk
from nltk.collocations import *
from nltk.tokenize import word_tokenize
from nltk import metrics
from spotify.utils.spotify_client import SpotifyClient


class LevenshteinReduce(object):
    def __init__(self, phrase, tracks):
        self.phrases = phrase
        self.tracks = tracks

    def get_most_similar_track(self):
        if self.tracks is None:
            return

        levenshteins = [
            {
                'levenshtein': metrics.edit_distance(self.phrases, track['name']),
                'url': track['url'],
                'name': track['name'],
                'artist': track['artist'],
                'image': track['image'],
                'phrase': self.phrases,
            }
            for track in self.tracks
        ]

        minimum_distance = None
        if levenshteins:
            minimum_distance = reduce(
                lambda d1, d2: d1 if d1['levenshtein'] < d2['levenshtein'] else d2,
                levenshteins
            )

        return minimum_distance


class LyricsTrack(object):
    def __init__(self, lyrics):
        self.lyrics = lyrics.lower()
        self.original_lyrics = self.lyrics
        self.spotify_client = SpotifyClient()
        self.last_ngrams = []
        self.acceptable_levenshtein = 3
        self.acquired_tracks = []

    def process(self, degree=3):
        self.degree = degree

        self._remove_punctuations()

        if degree == 3:
            ngrams = self._get_trigrams_with_collocation_pmi_for_lyrics()
        elif degree == 2:
            ngrams = self._get_bigrams_with_collocation_pmi_for_lyrics()
        else:
            ngrams = self.lyrics.split(' ')

        self.last_ngrams = ngrams

        ngram_tracks = []
        for ngram in ngrams:
            ngram_tracks.append({
                'phrase': ngram,
                'tracks': self.spotify_client.get_tracks(ngram),
            })

        phrase_to_tracks = []
        for ngram_track in ngram_tracks:
            phrase_to_tracks.append(LevenshteinReduce(
                phrase=ngram_track['phrase'],
                tracks=ngram_track['tracks']
            ).get_most_similar_track())

        for track in phrase_to_tracks:
            if track and track['levenshtein'] <= self.acceptable_levenshtein:
                self.acquired_tracks.append(track)
                self.lyrics = self.lyrics.replace(track['phrase'], '').strip()

        if self.lyrics.strip() != '':
            if len(self.last_ngrams) == len(ngrams):
                self.acceptable_levenshtein += 1

            self.degree -= 1
            self.process(self.degree)

    def get_tracks(self):
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
