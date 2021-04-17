from django import forms
from django.forms import Form, ModelForm, Textarea
from django.core.validators import MaxValueValidator, MinValueValidator 
from .models import CustomUser
from gui.models import Note, PatientYear, PatientDemographic
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User

# user authentication
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

# form to sign up new user for login view
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


# form to request additional patients for dashboard view
class RequestPatientsForm(Form):
    num_to_add = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], label = '')


# form to allow annotators to label individual note for annotation view
class NoteForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Note
        fields = [
            'Label'
        ]
        labels = {
            'Label': _('Please select your annotation for this note.'),
        }

# form to facilitate dynamic keyword highlighting for annotation view
class KeywordForm(Form):
    keywords = forms.CharField(widget = forms.Textarea(attrs={'style':'max-width: 90%; resize:vertical; resize: horizontal;','cols':25}), label = '')

# scratchpad for annotators
class ScratchpadForm(Form):
    scratchpad = forms.CharField(widget = forms.Textarea(attrs={'style':'max-width: 90%; resize:vertical; resize: horizontal;','cols':25}), label = '')

# form to allow annotators to label across patient year for annotation view
class PatientForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = PatientDemographic
        fields = [
            'SyndromicDiagnosis',
            'DementiaSeverity',
            'LabelCertainty',
        ]
        labels = {
            'SyndromicDiagnosis': _('Please input your syndromic diagnosis:'),
            'DementiaSeverity': _('Please input your dementia severity label:'),
            'LabelCertainty': _('How confident are you in this diagnosis?'),
        }


class ConsensusForm(Form):
    pass