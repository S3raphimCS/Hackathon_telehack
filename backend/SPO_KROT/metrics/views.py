from re import split as resplit

from datefinder import find_dates
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from openpyxl import load_workbook
from django.utils.translation import gettext_lazy as _
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Measurements, Operator, Report
from .serializers import ReportListSerializer, ReportDetailSerializer


class ReportDetailView(generics.RetrieveAPIView):
    """Возвращает информацию о конретном отчет по ID."""
    lookup_field = 'pk'
    queryset = Report.objects.all()
    serializer_class = ReportDetailSerializer


class ReportListView(generics.ListAPIView):
    """Возращает все отчеты."""
    queryset = Report.objects.all()
    serializer_class = ReportListSerializer


class ReportDownload(APIView):
    def post(self, request, *args, **kwargs):
        pass


# Подумать если будут кидать одинаковый отчет с разными названиями
@swagger_auto_schema(
    method='POST',
    operation_description=_("Создание случайного пароля"),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['filename', 'sheetname'],
        properties={
            'filename': openapi.Schema(type=openapi.TYPE_STRING),
            'sheetname': openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)
@api_view(["POST"])
def create_report(request):
    filename = request.data["filename"]
    sheetname = request.data['sheetname']
    parse_result = parse_excel(filename, sheetname)
    print(parse_result)
    if parse_result:
        report = Report.objects.create(title=filename, region=parse_result["region"],
                                       city=parse_result["city"], start_date=parse_result["start_date"],
                                       end_date=parse_result["end_date"], publisher=request.user)
        for metric in parse_result['metrics']:
            operator = Operator.objects.get_or_create(name=metric[0])[0]
            parse_metrics = metric[1]
            q = Measurements(operator=operator, report=report, voice_service_non_accessibility=parse_metrics[0],
                             voice_service_cut_off=parse_metrics[1], speech_quality_on_call=parse_metrics[2],
                             negative_mos_samples_ratio=parse_metrics[3], undelivered_messages=parse_metrics[4],
                             avg_sms_delivery_time=parse_metrics[5], http_failure_session=parse_metrics[6],
                             http_ul_mean_userdata_rate=parse_metrics[7], http_dl_mean_userdata_rate=parse_metrics[8],
                             http_session_time=parse_metrics[9], number_of_test_voice_connections=parse_metrics[10],
                             number_of_voice_sequences=parse_metrics[11],
                             voice_connections_with_low_intelligibility=parse_metrics[12],
                             number_of_sms_messages=parse_metrics[13],
                             number_of_connections_attempts_http=parse_metrics[14],
                             number_of_test_sessions_http=parse_metrics[15])
            q.save()
        return Response({'data': 'Отчет успешно добавлен!'}, status=status.HTTP_201_CREATED)

    else:
        return Response({"error": "Ошибка при работе с файлом"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def parse_excel(filename, sheetname):
    try:
        wb = load_workbook(filename)
        sheet = wb[sheetname]
    except FileNotFoundError:
        return FileNotFoundError("Файл не найден")  # "Файл не найден"
    except Exception as excp:
        return None  # f"Ошибка загрузки файла: {excp}"

    operators = {}

    try:
        region = ''.join(
            [word[0] for word in resplit(r'ФИЛИАЛ ФГУП «ГРЧЦ» В\w*', sheet["A8"].value)[1].lstrip().split()])
        start_date, end_date = [date.date().isoformat() for date in list(find_dates(sheet['A13'].value))]
        city = resplit(r':\w*', sheet["A14"].value)[1].lstrip()

        for count, value in enumerate('CDEFGHIJKLMNOP'):
            if sheet[f'{value}18'].value:
                values = []
                for j in range(19, 38):
                    if j == 23 or j == 26 or j == 31:
                        continue
                    else:
                        values.append(sheet[f'{value}{j}'].value)
                values = tuple(values)
                operators.update({sheet[f'{value}18'].value: values})

        metrics = [i for i in operators.items()]

        return {
            "start_date": start_date,
            "end_date": end_date,
            'region': region,
            "city": city,
            "metrics": metrics
        }

    except Exception as excp:
        return None  # f"Ошибка при парсинге: {excp}"


# ENDPOINT на обновление одной метрики
def download(request, excel):
    pass


@swagger_auto_schema(
    method='POST',
    operation_description=_("Изменяет все метрики одного отчета"),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['filename', 'sheetname'],
        properties={
            "measurements_set": openapi.Schema(type=openapi.TYPE_ARRAY,
                                               items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                                   'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                   'voice_service_non_accessibility': openapi.Schema(
                                                       type=openapi.TYPE_STRING),
                                                   'voice_service_cut_off': openapi.Schema(type=openapi.TYPE_STRING),
                                                   'speech_quality_on_call': openapi.Schema(type=openapi.TYPE_STRING),
                                                   'negative_mos_samples_ratio': openapi.Schema(
                                                       type=openapi.TYPE_STRING),
                                                   'undelivered_messages': openapi.Schema(type=openapi.TYPE_STRING),
                                                   'avg_sms_delivery_time': openapi.Schema(type=openapi.TYPE_STRING),
                                                   'http_failure_session': openapi.Schema(type=openapi.TYPE_STRING),
                                                   'http_ul_mean_userdata_rate': openapi.Schema(
                                                       type=openapi.TYPE_STRING),
                                                   'http_dl_mean_userdata_rate': openapi.Schema(
                                                       type=openapi.TYPE_STRING),
                                                   'http_session_time': openapi.Schema(type=openapi.TYPE_STRING),
                                                   'number_of_test_voice_connections': openapi.Schema(
                                                       type=openapi.TYPE_INTEGER),
                                                   'number_of_voice_sequences': openapi.Schema(
                                                       type=openapi.TYPE_INTEGER),
                                                   'voice_connections_with_low_intelligibility': openapi.Schema(
                                                       type=openapi.TYPE_INTEGER),
                                                   'number_of_sms_messages': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                   'number_of_connections_attempts_http': openapi.Schema(
                                                       type=openapi.TYPE_INTEGER),
                                                   'number_of_test_sessions_http': openapi.Schema(
                                                       type=openapi.TYPE_INTEGER),
                                               }, example=[
                                                   {
                                                       "id": 13,
                                                       "voice_service_non_accessibility": "0.294192888206702",
                                                       "voice_service_cut_off": "0.837628865979381",
                                                       "speech_quality_on_call": "4.170714857833180",
                                                       "negative_mos_samples_ratio": "0.252858176311110",
                                                       "undelivered_messages": "2.400000000000000",
                                                       "avg_sms_delivery_time": "6.276091028432380",
                                                       "http_failure_session": "2.161200101703530",
                                                       "http_ul_mean_userdata_rate": "2488.145512515050000",
                                                       "http_dl_mean_userdata_rate": "9700.979612662120000",
                                                       "http_session_time": "10.925764036688000",
                                                       "number_of_test_voice_connections": 7818,
                                                       "number_of_voice_sequences": 147909,
                                                       "voice_connections_with_low_intelligibility": 374,
                                                       "number_of_sms_messages": 500,
                                                       "number_of_connections_attempts_http": 1729,
                                                       "number_of_test_sessions_http": 2204}])),
        },
    )
)
@api_view(["POST"])
def update_report_metrics(request):
    """Изменяет все метрики одного отчета"""
    data = request.data
    # for metric in data["measurements_set"]:
    #     metric_id = metric["id"]
    #     voice_service_non_accessibility = metric["voice_service_non_accessibility"]
    #     voice_service_cut_off = metric["voice_service_cut_off"]
    #     speech_quality_on_call = metric["speech_quality_on_call"]
    #     negative_mos_samples_ratio = metric["negative_mos_samples_ratio"]
    #     undelivered_messages = metric["undelivered_messages"]
    #     avg_sms_delivery_time = metric["avg_sms_delivery_time"]
    #     http_failure_session = metric["http_failure_session"]
    #     http_ul_mean_userdata_rate = metric["http_ul_mean_userdata_rate"]
    #     http_dl_mean_userdata_rate = metric["http_dl_mean_userdata_rate"]
    #     http_session_time = metric["http_session_time"]
    #     number_of_test_voice_connections = metric["number_of_test_voice_connections"]
    #     number_of_voice_sequences = metric["number_of_voice_sequences"]
    #     voice_connections_with_low_intelligibility = metric["voice_connections_with_low_intelligibility"]
    #     number_of_sms_messages = metric["number_of_sms_messages"]
    #     number_of_connections_attempts_http = metric["number_of_connections_attempts_http"]
    #     number_of_test_sessions_http = metric["number_of_test_sessions_http"]
    #     # operator_id = metric["operator"]["id"]
    #     # report_id = metric["report"]["id"]
    #     Measurements.objects.filter(id=metric_id).update(
    #         voice_service_non_accessibility=voice_service_non_accessibility,
    #         voice_service_cut_off=voice_service_cut_off, speech_quality_on_call=speech_quality_on_call,
    #         negative_mos_samples_ratio=negative_mos_samples_ratio, undelivered_messages=undelivered_messages,
    #         avg_sms_delivery_time=avg_sms_delivery_time, http_failure_session=http_failure_session,
    #         http_ul_mean_userdata_rate=http_ul_mean_userdata_rate,
    #         http_dl_mean_userdata_rate=http_dl_mean_userdata_rate, http_session_time=http_session_time,
    #         number_of_test_voice_connections=number_of_test_voice_connections,
    #         number_of_voice_sequences=number_of_voice_sequences,
    #         voice_connections_with_low_intelligibility=voice_connections_with_low_intelligibility,
    #         number_of_sms_messages=number_of_sms_messages,
    #         number_of_connections_attempts_http=number_of_connections_attempts_http,
    #         number_of_test_sessions_http=number_of_test_sessions_http, )
