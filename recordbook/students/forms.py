from django import forms
from django.core.exceptions import ValidationError

from students.models import Group, Student


#class AddStudentForm(forms.Form):
#    last_name = forms.CharField(label='Фамилия', max_length=50)
#    first_name = forms.CharField(label='Имя', max_length=50)
#    middle_name = forms.CharField(label='Отчество', max_length=50)
#    email = forms.EmailField(label='e-mail')
#    birth_date = forms.DateField(label='Дата рождения')
#    is_study = forms.BooleanField(label='Учится', required=False, initial=True)
#    group = forms.ModelChoiceField(label='Группа', queryset=Group.objects.all(), empty_label='Не выбрана')
#    slug = forms.SlugField(label='URL', max_length=255)

class AddStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].empty_label = 'Не выбрана'

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise ValidationError('Недопустимые символы')
        return first_name
    class Meta:
        model = Student
        #fields = '__all__'
        fields = ['last_name', 'first_name', 'middle_name', 'email', 'birth_date', 'is_study', 'photo', 'group', 'slug']