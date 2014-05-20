__author__ = 'ankesh'
from django.contrib import admin
from plots.models import BenchmarkLogs, EmailLogs, EmailVerificationLogs, MachineInfo, Md5Log, RtAverage, RtBldg391, RtM35, RtMoss, RtSphflake, RtStar

admin.site.register(BenchmarkLogs)
admin.site.register(MachineInfo)
