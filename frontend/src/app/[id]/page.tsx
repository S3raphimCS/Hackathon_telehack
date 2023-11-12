"use client";

import React, { useEffect } from "react";
import { useForm, useFieldArray, SubmitHandler } from "react-hook-form";
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
import Button from "@mui/material/Button";
import { Report, MeasurementKeys } from "@/types/reports";
import { useUser } from "@/hooks/useUser";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { editReport, getReport } from "@/services/reports";
import { useMask } from "@react-input/mask";
import { toast } from "react-toastify";
import { useRouter } from "next/navigation";

const schema = z.object({
  region: z.string(),
  city: z.string(),
  start_date: z.date(),
  end_date: z.date(),
  measurements_set: z.array(
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
      http_dl_mean_userdata_rate: z.number(),
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

export default function ReportPage({ params }: { params: { id: number } }) {
  useUser();

  const {
    register,
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<Report>({
    resolver: zodResolver(schema),
  });

  const { fields } = useFieldArray({
    control,
    name: "measurements_set",
  });

  const { data, isLoading } = useQuery({
    queryKey: ["report", params.id],
    queryFn: () => getReport(params.id),
    refetchOnWindowFocus: false,
  });

  const queryClient = useQueryClient();
  const { mutate } = useMutation({
    mutationFn: (data: Report) => editReport(params.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reports"] });
      // queryClient.invalidateQueries({ queryKey: ["report", params.id] });
      toast.success("Успешно");
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });

  const onSubmit: SubmitHandler<Report> = (data) => {
    console.log(data);
    mutate(data);
  };

  useEffect(() => {
    reset(data);
  }, [data]);

  const headers = [];
  for (let i = 0; i < fields.length; i++) {
    headers.push(
      <TableCell key={`measurements_set.${i}.header`}>
        Значение
        <input type="hidden" {...register(`measurements_set.${i}.id`)} />
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

  const operatorCols = [
    <TableCell key="measurements_set.operator.name">
      {stringConsts.operator[0]}
    </TableCell>,
    <TableCell key="measurements_set.operator.constraints">
      {stringConsts.operator[1]}
    </TableCell>,
  ];
  for (let i = 0; i < fields.length; i++) {
    operatorCols.push(
      <TableCell key={`measurements_set.${i}.operator`}>
        {fields[i].operator.name}
      </TableCell>
    );
  }

  const rows = [
    <TableRow key="measurements_set.operator">{operatorCols}</TableRow>,
  ];

  for (let prop in fields[0]) {
    if (prop === "id" || prop === "report" || prop === "operator") continue;
    const cols = [
      <TableCell key={`measurements_set.${prop}.name`}>
        {stringConsts[prop as keyof MeasurementKeys][0]}
      </TableCell>,
      <TableCell key={`measurements_set.${prop}.constraints`}>
        {stringConsts[prop as keyof MeasurementKeys][1]}
      </TableCell>,
    ];
    for (let i = 0; i < fields.length; i++) {
      cols.push(
        <TableCell key={fields[i].id}>
          <TextField
            size="small"
            error={
              !!errors.measurements_set?.[i]?.[
                prop as keyof (typeof errors.measurements_set)[0]
              ]
            }
            InputLabelProps={{ shrink: true }}
            {...register(
              `measurements_set.${i}.${prop as keyof MeasurementKeys}`,
              { valueAsNumber: true }
            )}
          />
        </TableCell>
      );
    }
    rows.push(<TableRow key={`measurements_set.${prop}`}>{cols}</TableRow>);
  }

  const inputRef1 = useMask({
    mask: "гггг-мм-дд",
    replacement: { г: /\d/, м: /\d/, д: /\d/ },
    showMask: true,
    separate: true,
  });
  const inputRef2 = useMask({
    mask: "гггг-мм-дд",
    replacement: { г: /\d/, м: /\d/, д: /\d/ },
    showMask: true,
    separate: true,
  });

  const router = useRouter();

  return (
    <Box sx={{ p: 1 }}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Box sx={{ p: 1, display: "flex", justifyContent: "space-between" }}>
          <Box>
            <TextField
              label="Федеральный округ (ФО)"
              sx={{ width: "250px", mr: 2 }}
              size="small"
              {...register("region")}
              InputLabelProps={{ shrink: true }}
            />
            <TextField
              label="Место проведения контроля"
              sx={{ width: "400px" }}
              size="small"
              {...register("city")}
              InputLabelProps={{ shrink: true }}
            />
          </Box>
          <Box>
            <Button onClick={() => {router.push('/')}}>
              Назад
            </Button>
          </Box>
        </Box>
        <Typography sx={{ m: 1, color: "gray" }} variant="body1">
          Период проведения контроля
        </Typography>
        <Box sx={{ display: "flex", justifyContent: "space-between", p: 1 }}>
          <Box>
            <TextField
              label="C"
              sx={{ mr: 2 }}
              size="small"
              {...register("start_date", { valueAsDate: true })}
              InputLabelProps={{ shrink: true }}
              inputRef={inputRef1}
              error={!!errors.start_date}
            />
            <TextField
              label="По"
              size="small"
              {...register("end_date", { valueAsDate: true })}
              InputLabelProps={{ shrink: true }}
              inputRef={inputRef2}
              error={!!errors.end_date}
            />
          </Box>
          <Box>
            <Button type="submit" variant="contained">
              Сохранить
            </Button>
          </Box>
        </Box>
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
