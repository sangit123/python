from django import forms

class PagerForm(forms.Form):
    #filer = forms.CharField(max_length=1000,required=True,label='Filer Name',widget=forms.TextInput(attrs={'placeholder': 'e.g: qyfiler063a, lvfiler702a','class':'special', 'size': '25'}))
    CHOICES=[('idc','IDC'),
    		 ('us','US'),
    		 ('total','All')]
    shift = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),initial='idc')


    
    CHOICES=(('ics','ICS-INTUIT'),
    		 ('pcs','PCS-INTUIT'),
    		 ('mobile','CTO-MOBILE'))
    domain = forms.ChoiceField(choices=CHOICES)
