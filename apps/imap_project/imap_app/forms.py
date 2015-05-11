from django import forms

class FilerForm(forms.Form):
<<<<<<< HEAD
    filer = forms.CharField(max_length=1000,required=True,label='Filer Name',widget=forms.TextInput(attrs={'placeholder': 'e.g: qyfiler063a, lvfiler702a','class':'special', 'size': '25'}))
=======
    filer = forms.CharField(required=True,label='Filer Name')
>>>>>>> Checked in pagerstats v1. Working drilldown 1
    CHOICES=[('filer','Filer'),
    		 ('vfiler','vFiler')]
    Type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),initial='filer')
