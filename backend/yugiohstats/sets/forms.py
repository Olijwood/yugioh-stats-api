from django import forms 

class UserSubmittedBoosterPriceForm(forms.Form):
    price = forms.FloatField()

    def clean(self):
        cleaned_data = self.cleaned_data
        price = cleaned_data.get('price')
        cleaned_data['price'] = round(price, 2)
        return cleaned_data
    