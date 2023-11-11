from re import split as resplit

from datefinder import find_dates
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from openpyxl import load_workbook
from django.utils.translation import gettext_lazy as _
from rest_framework import status, generics, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import ExcelFile

from .models import Measurements, Operator, Report
from .serializers import ReportListSerializer, ReportDetailSerializer, ExcelUploadSerializer

update_metrics_example = [
    {
        "id": 13,
        "voice_service_non_accessibility": "0.3",
        "voice_service_cut_off": "0.8",
        "speech_quality_on_call": "4.2",
        "negative_mos_samples_ratio": "0.3",
        "undelivered_messages": "2.4",
        "avg_sms_delivery_time": "6.3",
        "http_failure_session": "2.2",
        "http_ul_mean_userdata_rate": "2488.1",
        "http_dl_mean_userdata_rate": "9700.9",
        "http_session_time": "10.9",
        "number_of_test_voice_connections": 7818,
        "number_of_voice_sequences": 147909,
        "voice_connections_with_low_intelligibility": 374,
        "number_of_sms_messages": 500,
        "number_of_connections_attempts_http": 1729,
        "number_of_test_sessions_http": 2204
    },
    {
        "id": 13,
        "voice_service_non_accessibility": "0.1",
        "voice_service_cut_off": "0.5",
        "speech_quality_on_call": "4.5",
        "negative_mos_samples_ratio": "0.1",
        "undelivered_messages": "2.8",
        "avg_sms_delivery_time": "6.6",
        "http_failure_session": "2.6",
        "http_ul_mean_userdata_rate": "2488.9",
        "http_dl_mean_userdata_rate": "9700.2",
        "http_session_time": "10.3",
        "number_of_test_voice_connections": 7818,
        "number_of_voice_sequences": 147909,
        "voice_connections_with_low_intelligibility": 374,
        "number_of_sms_messages": 500,
        "number_of_connections_attempts_http": 1729,
        "number_of_test_sessions_http": 2204
    }
]


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
# @swagger_auto_schema(
#     # method='POST',
#     operation_description=_("Создание случайного пароля"),
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=['filename', 'sheetname'],
#         properties={
#             'filename': openapi.Schema(type=openapi.TYPE_STRING),
#         },
#     )
# )
# @api_view(["POST"])
def create_report(filename, user):  # request
    # filename = request.data["filename"]
    parse_result = parse_excel(filename)
    if parse_result:
        report = Report.objects.create(title=filename, region=parse_result["region"],
                                       city=parse_result["city"], start_date=parse_result["start_date"],
                                       end_date=parse_result["end_date"], publisher=user)
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


def parse_excel(filename):
    try:
        wb = load_workbook(filename)
        sheet = wb.active
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
                        values.append(round(sheet[f'{value}{j}'].value, 1))
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


class ExcelUploadView(APIView):
    def post(self, request):
        serializer = ExcelUploadSerializer(data=request.data)
        if serializer.is_valid():
            excel = serializer.save()
            create_report(excel.file, request.user)
            ExcelFile.objects.filter(file=excel.file).delete()
            return Response({"data": "Данные успешно добавлены", }, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='PUT',
    operation_description=_("Изменяет все метрики одного отчета"),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=("__all__",),
        properties={
            'publisher': openapi.Schema(type=openapi.TYPE_STRING, example="Суперпользователь"),
            'region': openapi.Schema(type=openapi.TYPE_STRING, example="УФО"),
            'city': openapi.Schema(type=openapi.TYPE_STRING, example="г. Екатеринбург"),
            'start_date': openapi.Schema(type=openapi.FORMAT_DATE, example="2019-03-06"),
            'end_date': openapi.Schema(type=openapi.FORMAT_DATE, example="2019-07-23"),
            "measurements_set": openapi.Schema(type=openapi.TYPE_ARRAY,
                                               items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                                   'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                   'voice_service_non_accessibility': openapi.Schema(
                                                       type=openapi.FORMAT_DECIMAL),
                                                   'voice_service_cut_off': openapi.Schema(type=openapi.FORMAT_DECIMAL),
                                                   'speech_quality_on_call': openapi.Schema(type=openapi.FORMAT_DECIMAL),
                                                   'negative_mos_samples_ratio': openapi.Schema(
                                                       type=openapi.FORMAT_DECIMAL),
                                                   'undelivered_messages': openapi.Schema(type=openapi.FORMAT_DECIMAL),
                                                   'avg_sms_delivery_time': openapi.Schema(type=openapi.FORMAT_DECIMAL),
                                                   'http_failure_session': openapi.Schema(type=openapi.FORMAT_DECIMAL),
                                                   'http_ul_mean_userdata_rate': openapi.Schema(
                                                       type=openapi.FORMAT_DECIMAL),
                                                   'http_dl_mean_userdata_rate': openapi.Schema(
                                                       type=openapi.FORMAT_DECIMAL),
                                                   'http_session_time': openapi.Schema(type=openapi.FORMAT_DECIMAL),
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
                                               }, example=update_metrics_example)),
        },
    )
)
@api_view(["PUT"])
def update_report_metrics(request, pk):
    """Изменяет все метрики одного отчета"""
    data = request.data
    for el in data["measurements_set"][0]:
        metric = el
        metric_id = metric["id"]
        voice_service_non_accessibility = metric["voice_service_non_accessibility"]
        voice_service_cut_off = metric["voice_service_cut_off"]
        speech_quality_on_call = metric["speech_quality_on_call"]
        negative_mos_samples_ratio = metric["negative_mos_samples_ratio"]
        undelivered_messages = metric["undelivered_messages"]
        avg_sms_delivery_time = metric["avg_sms_delivery_time"]
        http_failure_session = metric["http_failure_session"]
        http_ul_mean_userdata_rate = metric["http_ul_mean_userdata_rate"]
        http_dl_mean_userdata_rate = metric["http_dl_mean_userdata_rate"]
        http_session_time = metric["http_session_time"]
        number_of_test_voice_connections = metric["number_of_test_voice_connections"]
        number_of_voice_sequences = metric["number_of_voice_sequences"]
        voice_connections_with_low_intelligibility = metric["voice_connections_with_low_intelligibility"]
        number_of_sms_messages = metric["number_of_sms_messages"]
        number_of_connections_attempts_http = metric["number_of_connections_attempts_http"]
        number_of_test_sessions_http = metric["number_of_test_sessions_http"]
        report_id = pk
        Report.objects.filter(id=report_id).update(region=data["region"], city=data["city"],
                                                   start_date=data["start_date"], end_date=data["end_date"], )
        Measurements.objects.filter(id=metric_id).update(
            voice_service_non_accessibility=voice_service_non_accessibility,
            voice_service_cut_off=voice_service_cut_off, speech_quality_on_call=speech_quality_on_call,
            negative_mos_samples_ratio=negative_mos_samples_ratio, undelivered_messages=undelivered_messages,
            avg_sms_delivery_time=avg_sms_delivery_time, http_failure_session=http_failure_session,
            http_ul_mean_userdata_rate=http_ul_mean_userdata_rate,
            http_dl_mean_userdata_rate=http_dl_mean_userdata_rate, http_session_time=http_session_time,
            number_of_test_voice_connections=number_of_test_voice_connections,
            number_of_voice_sequences=number_of_voice_sequences,
            voice_connections_with_low_intelligibility=voice_connections_with_low_intelligibility,
            number_of_sms_messages=number_of_sms_messages,
            number_of_connections_attempts_http=number_of_connections_attempts_http,
            number_of_test_sessions_http=number_of_test_sessions_http, )
    return Response({"data": "Данные успешно изменены"}, status=status.HTTP_200_OK)
