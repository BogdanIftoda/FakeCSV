from django import forms
from .models import Column, Schema


class SchemaForm(forms.ModelForm):

    class Meta:
        model = Schema
        fields = ('title', 'column_separator', 'string_character')


class ColumnForm(forms.ModelForm):

    def clean(self, *args, **kwargs):
        super(ColumnForm, self).clean()
        col_type = self.cleaned_data.get('column_type')
        if col_type == 'Integer':
            start_value = self.cleaned_data.get('start_value')
            end_value = self.cleaned_data.get('end_value')
            if start_value and end_value:
                if start_value >= end_value:
                    raise forms.ValidationError('the startValue must be less than the endValue')
                else:
                    return self.cleaned_data

    class Meta:
        model = Column
        fields = ('name', 'column_type', 'start_value', 'end_value', 'order')
