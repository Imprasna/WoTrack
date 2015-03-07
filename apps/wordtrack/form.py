from django import forms


class WordTrackForm(forms.Form):
    lyrics = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Please enter your text...'}
        ),
        required=True,
        label='Your Lyrics'
    )