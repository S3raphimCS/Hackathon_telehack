from re import split

from datefinder import find_dates
from django.shortcuts import render
from openpyxl import load_workbook

from .models import Measurements, Operator, Report


# Подумать если будут кидать одинаковый отчет с разными названиями
def create_report(request, filename, sheetname):
    parse_result = parse_excel(filename, sheetname)
    if parse_result:
        report = Report.objects.create(title=filename, region=parse_result["place"],
                                       start_date=parse_result["start_date"],
                                       end_date=parse_result["end_date"], publisher=request.user)
        for metric in parse_result['metrics']:
            operator = Operator.objects.get_or_create(name=metric[0])
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

    else:
        return "Ошибка при работе с файлом"


def parse_excel(filename, sheetname):
    try:
        wb = load_workbook(filename)
        sheet = wb[sheetname]
    except FileNotFoundError:
        return None  # "Файл не найден"
    except Exception as excp:
        return None  # f"Ошибка загрузки файла: {excp}"

    operators = {}

    try:
        date_values = sheet['A13'].value

        start_date, end_date = [date.date().isoformat() for date in list(find_dates(date_values))]
        place = split(r':\w*', sheet["A14"].value)[1].lstrip()

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
            "place": place,
            "metrics": metrics
        }

    except Exception as excp:
        return None  # f"Ошибка при парсинге: {excp}"

# ENDPOINT на обновление одной метрики
def download(request, excel):
    pass