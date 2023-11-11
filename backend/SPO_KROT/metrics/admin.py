from django.contrib import admin

from .models import Measurements, Operator, Report


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 15
    search_fields = ("name",)
    readonly_fields = ('id',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'city', 'start_date', 'end_date')
    list_per_page = 15
    search_fields = (
        'title', 'region', 'city', 'publisher__first_name', 'publisher__last_name', 'publisher__middle_name')
    readonly_fields = ('id',)
    list_filter = ('title', 'region', 'city', 'start_date', 'end_date')


@admin.register(Measurements)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('operator', 'report')
    fieldsets = (
        ('Параметры качества', {"fields": (
            'voice_service_non_accessibility', 'voice_service_cut_off', 'speech_quality_on_call',
            'negative_mos_samples_ratio')}),
        ("Показатели качества услуг подвижной радиотелефонной связи в части передачи коротких текстовых сообщений",
         {"fields": ('undelivered_messages', 'avg_sms_delivery_time',)}),
        (
            'Показатели качества услуг связи по передаче данных, за исключением услуг связи по передаче данных для целей передачи голосовой информации',
            {"fields": (
                'http_failure_session', 'http_ul_mean_userdata_rate', 'http_dl_mean_userdata_rate',
                'http_session_time')}),
        ("Справочная информация", {"fields": (
            'number_of_test_voice_connections', 'number_of_voice_sequences',
            'voice_connections_with_low_intelligibility',
            'number_of_sms_messages', 'number_of_connections_attempts_http', 'number_of_test_sessions_http')})
    )
    list_per_page = 20
    list_filter = ('operator', 'report__start_date', 'report__end_date', 'report__region', 'report__city')
    search_fields = ('operator', 'report__title', 'report__region', 'report__city')
