from django import forms
from django.contrib import admin

from .models import Choice
from .models import Question


class InlineChoice(admin.TabularInline):
    model = Choice
    extra = 1


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
    inlines = [
        InlineChoice
    ]


class ChoiceAdminForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'
        widgets = {

        }


@admin.register(Choice)
class ChoiceAdmin(SelectizeAdminMixin, admin.ModelAdmin):
    form = ChoiceAdminForm
    list_filter = (
        'question',
    )
    list_display_links = ('text',)
    list_display = (
        'question',
        'text',
        'votes',
    )
