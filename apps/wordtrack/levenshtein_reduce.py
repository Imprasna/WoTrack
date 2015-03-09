from nltk import metrics


class LevenshteinReduce(object):
    def __init__(self, phrase, tracks):
        """
        :param phrase: (str) phrase  or ngram
        :param tracks: (list) tacks to perform best string matching with
        :return: Returns the track from the list of tracks best matching the given phrase
        """
        self.phrases = phrase
        self.tracks = tracks

    def get_most_similar_track(self):
        """
        Determines the levenshtein distance between each track and phrase
        :return: track (object) the track with the smallest levenshtein with the phrase
        """
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