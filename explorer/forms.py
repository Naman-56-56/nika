from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        widget=forms.FileInput(attrs={
            'accept': '.csv',
            'class': 'form-control'
        }),
        help_text='Upload a CSV file for analysis'
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file:
            if not csv_file.name.endswith('.csv'):
                raise forms.ValidationError('Please upload a valid CSV file.')
        return csv_file


class ImageUploadForm(forms.Form):
    image_file = forms.FileField(
        label='Image File',
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'class': 'form-control'
        }),
        help_text='Upload an image file for analysis'
    )
    
    def clean_image_file(self):
        image_file = self.cleaned_data.get('image_file')
        if image_file:
            # Check if it's a valid image format
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
            file_extension = image_file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in valid_extensions:
                raise forms.ValidationError('Please upload a valid image file.')
        return image_file