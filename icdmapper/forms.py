from django import forms


class CutpasteForm(forms.Form):
    diagnosis = forms.CharField(max_length=None,
                                help_text='Paste the list of diagnosis here seperated by comma')
    source = forms.CharField(  # A hidden input for internal use
        max_length=20,  # tell from which page the user sent the message
        widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super(CutpasteForm, self).clean()
        diagnosis = cleaned_data.get('diagnosis')
        if not diagnosis:
            raise forms.ValidationError('You have to specify atleast one diagnosis')
