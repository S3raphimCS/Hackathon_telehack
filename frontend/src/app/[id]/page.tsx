"use client";

import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

interface Measurement {
  id: number;
  operator: {
    id: number;
    name: string;
  };
  voice_service_non_accessibility: number;
  voice_service_cut_off: number;
  speech_quality_on_call: number;
  negative_mos_samples_ratio: number;
  undelivered_messages: number;
  avg_sms_delivery_time: number;
  http_failure_session: number;
  http_ul_mean_userdata_rate: number;
  http_dl_mean_userdata_rate: number;
  http_session_time: number;
  number_of_test_voice_connections: number;
  number_of_voice_sequences: number;
  voice_connections_with_low_intelligibility: number;
  number_of_sms_messages: number;
  number_of_connections_attempts_http: number;
  number_of_test_sessions_http: number;
}

interface MeasurementKeys extends Omit<Measurement, "id"> {}

interface Report {
  region: string;
  place: string;
  from: string;
  to: string;
  measurements: Measurement[];
}

const schema = z.object({
  region: z.string(),
  place: z.string(),
  from: z.string(),
  to: z.string(),
  measurements: z.array(
    z.object({
      id: z.number(),
      voice_service_non_accessibility: z.number(),
      voice_service_cut_off: z.number(),
      speech_quality_on_call: z.number(),
      negative_mos_samples_ratio: z.number(),
      undelivered_messages: z.number(),
      avg_sms_delivery_time: z.number(),
      http_failure_session: z.number(),
      http_ul_mean_userdata_rate: z.number(),
      http_dl_mean_userdata_rate: z.number().min(80),
      http_session_time: z.number(),
      number_of_test_voice_connections: z.number(),
      number_of_voice_sequences: z.number(),
      voice_connections_with_low_intelligibility: z.number(),
      number_of_sms_messages: z.number(),
      number_of_connections_attempts_http: z.number(),
      number_of_test_sessions_http: z.number(),
    })
  ),
});

export default function ReportPage() {
  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<Report>({
    resolver: zodResolver(schema),
    defaultValues: {
      region: "УФО",
      place: "г. Екатеринбург",
      from: "01.01.2023",
      to: "01.03.2023",
      measurements: [
        {
          id: 1,
          operator: {
            id: 1,
            name: "Beeline",
          },
          voice_service_non_accessibility: 0.5,
          voice_service_cut_off: 0.2,
          speech_quality_on_call: 4.3,
          negative_mos_samples_ratio: 0.3,
          undelivered_messages: 4.3,
          avg_sms_delivery_time: 1,
          http_failure_session: 24.5,
          http_ul_mean_userdata_rate: 2466.8,
          http_dl_mean_userdata_rate: 1,
          http_session_time: 1,
          number_of_test_voice_connections: 1,
          number_of_voice_sequences: 1,
          voice_connections_with_low_intelligibility: 1,
          number_of_sms_messages: 1,
          number_of_connections_attempts_http: 1,
          number_of_test_sessions_http: 1,
        },
        {
          id: 2,
          operator: {
            id: 2,
            name: "MTS",
          },
          voice_service_non_accessibility: 0.5,
          voice_service_cut_off: 0.2,
          speech_quality_on_call: 4.3,
          negative_mos_samples_ratio: 0.3,
          undelivered_messages: 4.3,
          avg_sms_delivery_time: 1,
          http_failure_session: 24.5,
          http_ul_mean_userdata_rate: 2466.8,
          http_dl_mean_userdata_rate: 1,
          http_session_time: 1,
          number_of_test_voice_connections: 1,
          number_of_voice_sequences: 1,
          voice_connections_with_low_intelligibility: 1,
          number_of_sms_messages: 1,
          number_of_connections_attempts_http: 1,
          number_of_test_sessions_http: 1,
        },
      ],
    },
  });

  const { fields } = useFieldArray({
    control,
    name: "measurements",
  });

  const headers = [];
  for (let i = 0; i < fields.length; i++) {
    headers.push(
      <TableCell key={i}>
        Значение
        <input type="hidden" {...register(`measurements.${i}.id`)} />
      </TableCell>
    );
  }

  const stringConsts = {
    operator: [
      "Показатели качества услуг подвижной радиотелефонной связи в части голосового соединения",
    ],
    voice_service_non_accessibility: [
      "Доля неуспешных попыток установления голосового соединения",
      "не более 5",
    ],
    voice_service_cut_off: ["Доля обрывов голосовых соединений", "не более 5"],
    speech_quality_on_call: [
      "Средняя разборчивость речи на соединение",
      "не менее 2.6",
    ],
    negative_mos_samples_ratio: [
      "Доля голосовых соединений с низкой разборчивостью речи",
    ],
    undelivered_messages: ["Доля недоставленных SMS сообщений"],
    avg_sms_delivery_time: ["Среднее время доставки SMS сообщений"],
    http_failure_session: ["Доля неуспешных сессий по протоколу HTTP"],
    http_ul_mean_userdata_rate: [
      "Среднее значение скорости передачи данных от абонента",
    ],
    http_dl_mean_userdata_rate: [
      "Среднее значение скорости передачи данных к абоненту",
      "не менее 80",
    ],
    http_session_time: ["Продолжительность успешной сессии"],
    number_of_test_voice_connections: [
      "Общее количество тестовых голосовых соединений",
    ],
    number_of_voice_sequences: [
      "Общее количество голосовых последовательностей в оцениваемых соединениях",
    ],
    voice_connections_with_low_intelligibility: [
      "Количество голосовых соединений с низкой разборчивостью",
    ],
    number_of_sms_messages: ["Общее количество отправленных SMS - сообщений"],
    number_of_connections_attempts_http: [
      "Общее количество попыток соединений с сервером передачи данных HTTP",
    ],
    number_of_test_sessions_http: [
      "Общее количество тестовых сессий по протоколу HTTP",
    ],
  };

  const rows = [];
  const errorArr = [];
  for (let prop in fields[0]) {
    if (prop === "id") continue;
    const cols = [
      <TableCell key={`measurements.${prop}.name`}>
        {stringConsts[prop as keyof MeasurementKeys][0]}
      </TableCell>,
      <TableCell key={`measurements.${prop}.constraints`}>
        {stringConsts[prop as keyof MeasurementKeys][1]}
      </TableCell>,
    ];
    for (let i = 0; i < fields.length; i++) {
      cols.push(
        <TableCell key={fields[i].id}>
          {prop !== "operator" ? (
            <TextField
              size="small"
              defaultValue={fields[i][prop as keyof MeasurementKeys]}
              error={!!errors.measurements?.[i]?.[prop as keyof typeof errors.measurements[0]]}
              {...register(
                `measurements.${i}.${prop as keyof MeasurementKeys}`,
                { valueAsNumber: true }
              )}
            />
          ) : (
            fields[i].operator.name
          )}
        </TableCell>
      );
    }
    rows.push(<TableRow key={`measurements.${prop}`}>{cols}</TableRow>);
  }

  const onSubmit = (data: Report) => {
    console.log(data);
    console.log(errors);
  };

  return (
    <Box sx={{ p: 1 }}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <TextField
          label="Федеральный округ (ФО)"
          sx={{ m: 1, width: "250px" }}
          {...register("region")}
        />
        <TextField
          label="Место проведения контроля"
          sx={{ m: 1, width: "400px" }}
          {...register("place")}
        />
        <br />
        <Typography sx={{ m: 1, color: "gray" }} variant="body1">
          Период проведения контроля
        </Typography>
        <TextField label="C" sx={{ m: 1 }} {...register("from")} />
        <TextField label="По" sx={{ m: 1 }} {...register("to")} />
        <input type="submit" />
        <TableContainer component={Paper} sx={{ m: 1 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Параметы качества</TableCell>
                <TableCell>Требования к граничным значениям</TableCell>
                {headers}
              </TableRow>
            </TableHead>
            <TableBody>{rows}</TableBody>
          </Table>
        </TableContainer>
      </form>
    </Box>
  );
}
