# from django import forms
# from blog.models import Post,Comment

# class PostForm(forms.ModelForm):
#     class Meta():
#         model=Post
#         fields=('author','title','text')
#         widgets={'title':forms.TextInput(attrs={'class':'textinputclass'}),
#         'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})}




# class CommentForm(forms.ModelForm):
#     class Meta():
#         model=Comment
#         fields=('author','text')

#         widgets={
#             'author':forms.TextInput(attrs={'class':'textinputclass'}),
#         'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
#         }

from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',  # Bootstrap class for input
                'placeholder': 'Enter the title of your post',  # Placeholder for better user experience
                'style': 'max-width: 500px;',  # Custom style to limit the width of the title
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',  # Bootstrap class for text area
                'placeholder': 'Write your post content here...',  # Placeholder for content
                'style': 'min-height: 200px; max-width: 500px;',  # Custom styles to adjust height and width
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ( 'text',)
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',  # Bootstrap class for input
                'placeholder': 'Your Name',  # Placeholder for comment author
                'style': 'max-width: 300px;',  # Custom style to limit the width of the name input
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',  # Bootstrap class for text area
                'placeholder': 'Write your comment here...',  # Placeholder for comment text
                'style': 'min-height: 100px; max-width: 500px;',  # Custom styles to adjust height and width
            }),
        }
