from django import forms
from django.contrib import admin
from selectize.widgets import RemoteSelectize
from .models import Choice
from .models import Question


class SelectizeAdminMixin(object):
    class Media:
        js = (
            'selectize.js',
        )


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {

        }


@admin.register(Question)
class QuestionAdmin(SelectizeAdminMixin, admin.ModelAdmin):
    form = QuestionAdminForm


class ChoiceAdminForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'
        widgets = {
            'question': RemoteSelectize.make_from_model(Question)
        }


@admin.register(Choice)
class ChoiceAdmin(SelectizeAdminMixin, admin.ModelAdmin):
    form = ChoiceAdminForm
