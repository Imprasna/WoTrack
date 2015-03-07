from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from apps.wordtrack.form import WordTrackForm
from apps.wordtrack.lyrics_track import LyricsTrack


class WordTrackView(View):

    def get(self, request):
        view_data = {
            'tracks': [],
            'form': WordTrackForm()
        }
        return render(request, 'home.html', view_data)

    def post(self, request):
        wordtrack_form = WordTrackForm({
            'lyrics': request.POST.get('lyrics')
        })

        view_data = {
            'tracks': [],
        }

        if not wordtrack_form.is_valid():
            return JsonResponse(view_data)

        lyrics_track = LyricsTrack(wordtrack_form.cleaned_data['lyrics'])
        lyrics_track.process()
        view_data['tracks'] = lyrics_track.get_tracks()

        return JsonResponse(view_data)
