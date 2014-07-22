__author__ = 'ankesh'

from django import forms
from plots.models import BenchmarkLogs, MachineInfo


class ComparisonFilterForm(forms.Form):
    os = forms.ChoiceField(label='Operating System', choices=[(x['ostype'], x['ostype']) for x in MachineInfo.objects.values('ostype').distinct()])
    n_processors = forms.ChoiceField(label='Number of Processors', choices=[(x['processors'], x['processors']) for x in MachineInfo.objects.values('processors').distinct()])
    processor_family = forms.ChoiceField(label='Processor Family', choices=[(x['vendor_id'], x['vendor_id']) for x in MachineInfo.objects.values('vendor_id').distinct()])
    processor_model = forms.ChoiceField(label='Processor Family', choices=[(x['model_name'], x['model_name']) for x in MachineInfo.objects.values('model_name').distinct()])
    date_submitted = forms.ChoiceField(label='Date Submitted', choices=[('this_week', 'This Week'), ('this_month', 'This Month'), ('this_year', 'This Year'), ('all_time', 'All Time')])



