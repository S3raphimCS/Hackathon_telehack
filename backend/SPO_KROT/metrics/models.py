from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Operator(models.Model):
    """Модель операторов связи для возможности добавления новых."""
    class Meta:
        verbose_name = "Оператор"
        verbose_name_plural = "Операторы"

    name = models.CharField(
        _("Название оператора"),
        max_length=50,
        blank=False, null=False,
        unique=True,
    )

    def __str__(self) -> models.CharField:
        return self.name


class Report(models.Model):
    """Модель отчетов для потенциального хранения информации об отчетах в БД."""
    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

    title = models.CharField(
        _("Название отчета"),
        max_length=200,
        blank=False, null=False,
    )
    region = models.CharField(
        _("Регион"),
        max_length=100,
        blank=True, null=True
    )
    start_date = models.DateField(
        _("Дата начала измерений"),
        blank=True, null=True,
    )
    end_date = models.DateField(
        _("Дата конца измерений"),
        blank=True, null=True,
    )
    publisher = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )
    published = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.start_date}-{self.end_date} {self.title}"


class Measurements(models.Model):
    """Модель записи измерений из отчета, которые будут изменяться."""
    class Meta:
        verbose_name = "Измерение"
        verbose_name_plural = "Измерения"

    operator = models.ForeignKey(
        Operator,
        on_delete=models.CASCADE,
    )
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
    )
    voice_service_non_accessibility = models.DecimalField(
        _("Доля неуспешных попыток установления голосового соединения"),
        decimal_places=15,
        max_digits=30,
        validators=PERCENTAGE_VALIDATOR
    )
    voice_service_cut_off = models.DecimalField(
        _("Доля обрывов голосовых соединений"),
        decimal_places=15,
        max_digits=30,
        validators=PERCENTAGE_VALIDATOR
    )
    speech_quality_on_call = models.DecimalField(
        _("Средняя разборчивость речи на соединение"),
        decimal_places=15,
        max_digits=30,
    )
    negative_mos_samples_ratio = models.DecimalField(
        _("Доля голосовых соединений с низкой разборчивостью речи"),
        decimal_places=15,
        max_digits=30,
        validators=PERCENTAGE_VALIDATOR
    )
    undelivered_messages = models.DecimalField(
        _("Доля недоставленных SMS сообщений"),
        decimal_places=15,
        max_digits=30,
        validators=PERCENTAGE_VALIDATOR
    )
    avg_sms_delivery_time = models.DecimalField(
        _("Среднее время доставки SMS сообщений"),
        decimal_places=15,
        max_digits=30,
    )
    http_failure_session = models.DecimalField(
        _("Доля неуспешных сессий по протоколу HTTP"),
        decimal_places=15,
        max_digits=30,
        validators=PERCENTAGE_VALIDATOR
    )
    http_ul_mean_userdata_rate = models.DecimalField(
        _("Среднее значение скорости передачи данных от абонента"),
        decimal_places=15,
        max_digits=30,
    )
    http_dl_mean_userdata_rate = models.DecimalField(
        _("Среднее значение скорости передачи данных к абоненту"),
        decimal_places=15,
        max_digits=30,
    )
    http_session_time = models.DecimalField(
        _("Продолжительность успешной сессии"),
        decimal_places=15,
        max_digits=30,
    )
    number_of_test_voice_connections = models.IntegerField(
        _("Общее количество тестовых голосовых соединений "),
    )
    number_of_voice_sequences = models.IntegerField(
        _("Общее количество голосовых последовательностей в оцениваемых соединениях"),
    )
    voice_connections_with_low_intelligibility = models.IntegerField(
        _("Количество голосовых соединений с низкой разборчивостью"),
    )
    number_of_sms_messages = models.IntegerField(
        _("Общее количество отправленных SMS - сообщений"),
    )
    number_of_connections_attempts_http = models.IntegerField(
        _("Общее количество попыток соединений с сервером передачи данных HTTP"),
    )
    number_of_test_sessions_http = models.IntegerField(
        _("Общее количество тестовых сессий по протоколу HTTP"),
    )

    def __str__(self):
        return f"Метрика {self.operator} из отчета {self.report}"
