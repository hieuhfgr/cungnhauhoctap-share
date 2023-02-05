from django import forms

from myfunc.myfunc import getBadwords
badwords = getBadwords()

#post
class CreatePostForm(forms.Form):
    title = forms.CharField(label="Tiêu đề bài viết", max_length=255)
    content = forms.CharField(label="Nội dung bài viết", widget=forms.Textarea ,min_length=10)

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

class ChangePostForm(forms.Form):
    title = forms.CharField(label="Tiêu đề bài viết", max_length=255)
    content = forms.CharField(label="Nội dung bài viết", widget=forms.Textarea ,min_length=10)

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

class QuestionForm(forms.Form):
    question = forms.CharField(label='Câu hỏi của bạn')

    def clean_question(self):
        question = self.cleaned_data['question'].lower()
        for word in badwords:
            if question.find(word.word) != -1:
                raise forms.ValidationError('Câu hỏi của bạn chứa từ ngữ không phù hợp')
        
        return self.cleaned_data['question']

class AnswerForm(forms.Form):
    answer = forms.CharField(label='Câu trả lời của bạn')

    def clean_answer(self):
        answer = self.cleaned_data['answer'].lower()
        for word in badwords:
            if answer.find(word.word) != -1:
                raise forms.ValidationError('Câu trả lời của bạn chứa từ ngữ không phù hợp')
        
        return self.cleaned_data['answer']

class SendMessageForm(forms.Form):
    message = forms.CharField(label='Nhập tin nhắn:')

    def clean_message(self):
        message = self.cleaned_data['message'].lower()
        for word in badwords:
            if message.find(word.word) != -1:
                raise forms.ValidationError('tin nhắn của bạn chứa từ ngữ không phù hợp')
        
        return self.cleaned_data['message']

#test
class CreateTestForm(forms.Form):
    title = forms.CharField(label="Tiêu đề Kiểm Tra", max_length=255)
    content = forms.CharField(label="Nội dung Kiểm Tra", widget=forms.Textarea ,min_length=10)

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


class ChangeTestForm(forms.Form):
    title = forms.CharField(label="Tiêu đề Kiểm Tra", max_length=255)
    content = forms.CharField(label="Nội dung Kiểm Tra", widget=forms.Textarea ,min_length=10)

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