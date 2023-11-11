from django.contrib import admin

from .models import Measurements, Operator, Report


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(Measurements)
class MeasurementAdmin(admin.ModelAdmin):
    pass
