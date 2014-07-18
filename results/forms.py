__author__ = 'ankesh'

from django import forms
from plots.models import BenchmarkLogs, MachineInfo


class ComparisonFilterForm(forms.Form):
    os = forms.ChoiceField(choices=[(x['ostype'], x['ostype']) for x in MachineInfo.objects.values('ostype').distinct()])
    n_processors = forms.ChoiceField(choices=[(x['processors'], x['processors']) for x in MachineInfo.objects.values('processors').distinct()])
    processor_family = forms.ChoiceField(choices=[(x['vendor_id'], x['vendor_id']) for x in MachineInfo.objects.values('vendor_id').distinct()])
    processor_model = forms.ChoiceField(choices=[(x['model_name'], x['model_name']) for x in MachineInfo.objects.values('model_name').distinct()])


