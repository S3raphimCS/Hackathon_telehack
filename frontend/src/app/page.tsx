"use client";

import React from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import Link from "next/link";
import AddReportForm from "@/components/AddReportForm";
import { useUser } from "@/hooks/useUser";
import { useQuery } from "@tanstack/react-query";
import { getReports } from "@/services/reports";

export default function Home() {
  useUser();

  const [open, setOpen] = React.useState<boolean>(false);
  const [page, setPage] = React.useState<number>(0);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const { isLoading, data, error, isFetching } = useQuery({
    queryKey: ["reports", page],
    queryFn: () => getReports(15, 15 * page),
    staleTime: 5000,
  });

  return (
    <>
      <main>
        <Box sx={{ p: 1, display: "flex", justifyContent: "space-between" }}>
          <Box>
            <Button variant="contained" sx={{ mr: 1 }} onClick={handleOpen}>
              Добавить отчет
            </Button>
          </Box>
          <Box>
            <Button disabled={!Boolean(data?.previous) && !isFetching} sx={{ mr: 1 }} onClick={() => {setPage((page) => page - 1)}}>
              Предыдущая страница
            </Button>
            <Button disabled={!Boolean(data?.next) && !isFetching} onClick={() => {setPage((page) => page + 1)}}>Следующая страница</Button>
          </Box>
        </Box>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell align="center">Федеральный округ ФО</TableCell>
                <TableCell align="center">Место проведения контроля</TableCell>
                <TableCell align="center">Период проведения</TableCell>
                <TableCell align="center">Просмотр отчета</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data?.results.map((report) => (
                <TableRow>
                  <TableCell scope="row" align="center">
                    {report.region}
                  </TableCell>
                  <TableCell align="center">{report.city}</TableCell>
                  <TableCell align="center">
                    {report.start_date} - {report.end_date}
                  </TableCell>
                  <TableCell align="center">
                    <Button LinkComponent={Link} href={`/${report.id}`}>
                      Просмотреть
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </main>
      <AddReportForm open={open} handleClose={handleClose} />
    </>
  );
}
