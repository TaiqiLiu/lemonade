from django import forms

#Used to try the special form function of django, and finally gave up
class record_form(forms.Form):

    name=forms.CharField(label='name',min_length=1,max_length=50,error_messages={"required":"Stuff doesn't exits"})
    beverage=forms.CharField(label='beverage',min_length=1,max_length=50,error_messages={"required":"Beverage doesn't exits"})
    quantity=forms.CharField(label='quantity',min_length=1,max_length=5,error_messages={"required":"Quantity wrong"})