from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'url', 'body', 'test']
        widgets = {
            'test': forms.widgets.TextInput(
                attrs={
                    'placeholder': "Type 'yes' here"}),
            'url': forms.widgets.URLInput(
                attrs={
                    'placeholder': 'http://'})}

        labels = {'test': 'Are you human?', 'url': 'URL (Optional)'}

    def __init__(self, **kwargs):
        d = kwargs.get('data')
        if d and d.get('submit') == 'Submit':
            self.is_preview = False

        else:
            self.is_preview = True

        super().__init__(**kwargs)

    def clean_test(self):
        t = self.cleaned_data.get('test')
        if t != 'yes':
            raise forms.ValidationError("Are you a human? Type 'yes'")
        return t

    def clean_body(self):
        # check for spam here someday
        b = self.cleaned_data.get('body')
        if False:
            raise forms.ValidationError("This looks like spam!")
        return b

    def clean(self):
        super().clean()
        if self.is_preview:
            raise forms.ValidationError(
                "Preview your comment, then hit submit!")
