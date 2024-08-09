# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User, Student, Practitioner
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
# from django import forms
# from .models import Recording, StudyMaterial
# from .models import Assignment, Submission
# class StudentSignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True, help_text='First name')
#     last_name = forms.CharField(max_length=30, required=True, help_text='Last name')
#     email = forms.EmailField(max_length=254, required=True, help_text='Email')

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Register'))

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_student = True
#         if commit:
#             user.save()
#             Student.objects.create(user=user)
#         return user

# class PractitionerSignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True, help_text='First name')
#     last_name = forms.CharField(max_length=30, required=True, help_text='Last name')
#     email = forms.EmailField(max_length=254, required=True, help_text='Email')

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Register'))



#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')
#         username = cleaned_data.get('username')

#         if password1 and password2 and password1 != password2:
#             self.add_error('password2', "Passwords do not match.")

#         if User.objects.filter(username=username).exists():
#             self.add_error('username', "A user with that username already exists.")

#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_practitioner = True
#         if commit:
#             user.save()
#             Practitioner.objects.create(user=user)
#         return user

# class RecordingForm(forms.ModelForm):
#     class Meta:
#         model = Recording
#         fields = ['title', 'description', 'confession']

#     title = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'E.g. Introduction to GPT-4',
#             'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4 rounded-r-none border-r-0 pr-2 text-base font-normal leading-normal'
#         })
#     )

#     description = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={
#             'placeholder': 'E.g. This is the first in a series of lectures on GPT-4. We\'ll cover its evolution, key features, and how to use it in practice.',
#             'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none min-h-36 placeholder:text-[#49779c] p-4 text-base font-normal leading-normal'
#         })
#     )

#     confession = forms.FileField(
#         required=True,
#         widget=forms.ClearableFileInput(attrs={
#             'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4'
#         })
#     )



# class StudyMaterialForm(forms.ModelForm):
#     class Meta:
#         model = StudyMaterial
#         fields = ['title', 'description', 'file']

#     title = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'E.g. Introduction to GPT-4',
#             'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4 rounded-r-none border-r-0 pr-2 text-base font-normal leading-normal'
#         })
#     )

#     description = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={
#             'placeholder': 'E.g. This is the first in a series of lectures on GPT-4. We\'ll cover its evolution, key features, and how to use it in practice.',
#             'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none min-h-36 placeholder:text-[#49779c] p-4 text-base font-normal leading-normal'
#         })
#     )

#     file = forms.FileField(
#         required=True,
#         widget=forms.ClearableFileInput(attrs={
#             'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4'
#         })
#     )


# class AssignmentForm(forms.ModelForm):
#     class Meta:
#         model = Assignment
#         fields = ['title', 'description', 'file']

#     title = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'E.g. Introduction to GPT-4',
#             'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4 rounded-r-none border-r-0 pr-2 text-base font-normal leading-normal'
#         })
#     )

#     description = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={
#             'placeholder': 'E.g. This is the first in a series of lectures on GPT-4. We\'ll cover its evolution, key features, and how to use it in practice.',
#             'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none min-h-36 placeholder:text-[#49779c] p-4 text-base font-normal leading-normal'
#         })
#     )

#     file = forms.FileField(
#         required=True,
#         widget=forms.ClearableFileInput(attrs={
#             'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4'
#         })
#     )

        
  

# class SubmissionForm(forms.ModelForm):
#     class Meta:
#         model = Submission
#         fields = ['file']
#         widgets = {

#             'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Practitioner
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Recording

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='First name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last name')
    email = forms.EmailField(max_length=254, required=True, help_text='Email')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
            Student.objects.create(user=user)
        return user

class PractitionerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='First name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last name')
    email = forms.EmailField(max_length=254, required=True, help_text='Email')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))



    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        if User.objects.filter(username=username).exists():
            self.add_error('username', "A user with that username already exists.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_practitioner = True
        if commit:
            user.save()
            Practitioner.objects.create(user=user)
        return user




# myapp/forms.py
from django import forms
from .models import Recording

class RecordingForm(forms.ModelForm):
    class Meta:
        model = Recording
        fields = ['title', 'description', 'confession']

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Introduction to GPT-4',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4 rounded-r-none border-r-0 pr-2 text-base font-normal leading-normal'
        })
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'E.g. This is the first in a series of lectures on GPT-4. We\'ll cover its evolution, key features, and how to use it in practice.',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none min-h-36 placeholder:text-[#49779c] p-4 text-base font-normal leading-normal'
        })
    )

    confession = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4'
        })
    )

from .models import Recording, StudyMaterial













class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'file']

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Introduction to GPT-4',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4 rounded-r-none border-r-0 pr-2 text-base font-normal leading-normal'
        })
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'E.g. This is the first in a series of lectures on GPT-4. We\'ll cover its evolution, key features, and how to use it in practice.',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none min-h-36 placeholder:text-[#49779c] p-4 text-base font-normal leading-normal'
        })
    )

    file = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4'
        })
    )







from django import forms
from .models import Assignment, Submission

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'file']

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Introduction to GPT-4',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4 rounded-r-none border-r-0 pr-2 text-base font-normal leading-normal'
        })
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'E.g. This is the first in a series of lectures on GPT-4. We\'ll cover its evolution, key features, and how to use it in practice.',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none min-h-36 placeholder:text-[#49779c] p-4 text-base font-normal leading-normal'
        })
    )

    file = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d151c] focus:outline-0 focus:ring-0 border-none bg-[#e7eef4] focus:border-none h-14 placeholder:text-[#49779c] p-4'
        })
    )

        
  

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }