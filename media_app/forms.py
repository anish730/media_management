from django import forms
from .models import MediaFile

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['file']

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        valid_extensions = ['mp3', 'mp4', 'jpeg', 'png', 'gif', 'jpg']
        file_extension = uploaded_file.name.split('.')[-1].lower()
        file_size = uploaded_file.size

        # Validate file extension
        if file_extension not in valid_extensions:
            raise forms.ValidationError('Invalid file extension.')

        # Validate file size
        if file_size > 10 * 1024 * 1024 or file_size < 100 * 1024:
            raise forms.ValidationError('File size must be between 100KB and 10MB.')

        return uploaded_file