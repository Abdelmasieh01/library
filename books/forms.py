from django import forms
from .models import Book, Borrowing

class DateInput(forms.DateInput):
    input_type = 'date'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['category', 'code', 'name', 'author', 'copies', 'age_category']

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['category', 'code', 'available']

'''
class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['name']
'''

class BorrowingForm(forms.ModelForm):
    category = forms.IntegerField(min_value=200, label='الرقم العام للكتاب')
    code = forms.IntegerField(min_value=0, label='الرقم الخاص للكتاب')
    class Meta:
        model = Borrowing
        fields = ['borrower', 'borrow_date']
        widgets = {
            'borrow_date': DateInput()
        }

class ReturnForm(forms.Form):
    borrowing = forms.ModelChoiceField(queryset=Borrowing.objects.all().exclude(returned=True), label='طلب الاستعارة')
    return_date = forms.DateField(widget=DateInput(), label='تاريخ الإرجاع')

    
