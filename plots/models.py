# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models


class BenchmarkLogs(models.Model):
    id = models.IntegerField(primary_key=True)
    machine_desc = models.CharField(max_length=765, blank=True)
    brlcad_version = models.CharField(max_length=45, blank=True)
    running_time = models.IntegerField(null=True, blank=True)
    time_of_execution = models.DateTimeField()
    approx_vgr = models.FloatField(null=True, blank=True)
    log_vgr = models.FloatField(null=True, blank=True)
    params = models.CharField(max_length=765, blank=True)
    results = models.CharField(max_length=765, blank=True)
    compiler_flags = models.TextField(blank=True)
    complete_info = models.TextField(blank=True)
    class Meta:
        db_table = u'benchmark_logs'


class EmailLogs(models.Model):
    imap_id = models.IntegerField(null=True, blank=True)
    md5 = models.CharField(max_length=300, blank=True)
    time = models.DateTimeField()
    class Meta:
        db_table = u'email_logs'


class EmailVerificationLogs(models.Model):
    verified_till = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField()
    class Meta:
        db_table = u'email_verification_logs'


class MachineInfo(models.Model):
    benchmark = models.OneToOneField(BenchmarkLogs, blank=True, primary_key=True)
    osrelease = models.CharField(max_length=300, blank=True)
    cpu_mhz = models.FloatField(null=True, blank=True)
    hostname = models.CharField(max_length=300, blank=True)
    cores = models.IntegerField(null=True, blank=True)
    processors = models.IntegerField(null=True, blank=True)
    physical_addr_size = models.IntegerField(null=True, blank=True)
    virtual_addr_size = models.IntegerField(null=True, blank=True)
    vendor_id = models.CharField(max_length=300, blank=True)
    ostype = models.CharField(max_length=300, blank=True)
    model_name = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u'machine_info'


class Md5Log(models.Model):
    benchmark = models.ForeignKey(BenchmarkLogs, blank=True, primary_key=True)
    file_name = models.CharField(max_length=765, blank=True)
    md5sum = models.CharField(max_length=300, blank=True)
    archived = models.CharField(max_length=9, blank=True)
    db_entries = models.CharField(max_length=9, blank=True)
    class Meta:
        db_table = u'md5_log'


class RtAverage(models.Model):
    benchmark = models.ForeignKey(BenchmarkLogs, blank=True, primary_key=True)
    abs_rps = models.FloatField(null=True, blank=True)
    vgr_rps = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=57, blank=True)
    class Meta:
        db_table = u'rt_average'


class RtBldg391(models.Model):
    benchmark = models.ForeignKey(BenchmarkLogs, primary_key=True, blank=True)
    abs_rps = models.FloatField(null=True, blank=True)
    vgr_rps = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=57, blank=True)
    class Meta:
        db_table = u'rt_bldg391'


class RtM35(models.Model):
    benchmark = models.ForeignKey(BenchmarkLogs, primary_key=True, blank=True)
    abs_rps = models.FloatField(null=True, blank=True)
    vgr_rps = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=57, blank=True)
    class Meta:
        db_table = u'rt_m35'


class RtMoss(models.Model):
    benchmark = models.ForeignKey(BenchmarkLogs, primary_key=True, blank=True)
    abs_rps = models.FloatField(null=True, blank=True)
    vgr_rps = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=57, blank=True)
    class Meta:
        db_table = u'rt_moss'


class RtSphflake(models.Model):
    benchmark = models.ForeignKey(BenchmarkLogs, primary_key=True, blank=True)
    abs_rps = models.FloatField(null=True, blank=True)
    vgr_rps = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=57, blank=True)
    class Meta:
        db_table = u'rt_sphflake'


class RtStar(models.Model):
    benchmark = models.ForeignKey(BenchmarkLogs, primary_key=True, blank=True)
    abs_rps = models.FloatField(null=True, blank=True)
    vgr_rps = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=57, blank=True)
    class Meta:
        db_table = u'rt_star'


class RtWorld(models.Model):
    benchmark = models.ForeignKey(BenchmarkLogs, primary_key=True, blank=True)
    abs_rps = models.FloatField(null=True, blank=True)
    vgr_rps = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=57, blank=True)
    class Meta:
        db_table = u'rt_world'

