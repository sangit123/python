from django import forms

class SilencerForm(forms.Form):
    #filer = forms.CharField(max_length=1000,required=True,label='Filer Name',widget=forms.TextInput(attrs={'placeholder': 'e.g: qyfiler063a, lvfiler702a','class':'special', 'size': '25'}))
    
    
    
    CHOICES=[('qdc','QDC'),
          ('lvdc','LVDC')]
    datacenter = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),initial='qdc')
