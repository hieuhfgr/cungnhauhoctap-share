from django import forms
from myfunc.myfunc import getBadwords
badwords = getBadwords()

#post
class CreateShareForm(forms.Form):
    title = forms.CharField(label="Tiêu đề", max_length=255)
    content = forms.CharField(label="Nội dung", widget=forms.Textarea ,min_length=10)

    def clean_title(self):
        title = self.cleaned_data['title'].lower()
        for word in badwords:
            if title.find(word.word) != -1:
                raise forms.ValidationError('Tiêu đề của bạn chứa từ ngữ không phù hợp')
        return self.cleaned_data['title']
    def clean_content(self):
        content = self.cleaned_data['content'].lower()
        for word in badwords:
            if content.find(word.word) != -1:
                raise forms.ValidationError('Nội dung của bạn chứa từ ngữ không phù hợp')
        return self.cleaned_data['content']

class ChangeShareForm(forms.Form):
    title = forms.CharField(label="Tiêu đề", max_length=255)
    content = forms.CharField(label="Nội dung", widget=forms.Textarea ,min_length=10)

    def clean_title(self):
        title = self.cleaned_data['title'].lower()
        for word in badwords:
            if title.find(word.word) != -1:
                raise forms.ValidationError('Tiêu đề của bạn chứa từ ngữ không phù hợp')
        return self.cleaned_data['title']
    def clean_content(self):
        content = self.cleaned_data['content'].lower()
        for word in badwords:
            if content.find(word.word) != -1:
                raise forms.ValidationError('Nội dung của bạn chứa từ ngữ không phù hợp')
        return self.cleaned_data['content']