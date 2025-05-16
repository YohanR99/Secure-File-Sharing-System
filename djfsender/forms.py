from django import forms
from .models import FileSender, Department  # ✅ Import Department model
from .utilities.validate_files import check_file


class FileSenderForm(forms.ModelForm):
    file = forms.FileField(
        validators=[check_file],
        widget=forms.FileInput(attrs={'class': 'account-setting__avatar'}),
        label="Select File"
    )

    file_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form__field form__field--textarea',
                'placeholder': 'File Description',
                'cols': '10',
                'rows': '8',
            }
        ),
        label="File Description"
    )

    departments_allowed = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Allowed Departments"
    )

    class Meta:
        model = FileSender
        fields = ['file', 'file_description', 'departments_allowed']
