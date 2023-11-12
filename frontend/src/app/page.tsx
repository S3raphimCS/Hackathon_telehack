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
import TableSortLabel from "@mui/material/TableSortLabel";
import { Sort } from "@/types/reports";
import TablePagination from "@mui/material/TablePagination";
import TextField from "@mui/material/TextField";

export default function Home() {
  useUser();

  const [open, setOpen] = React.useState<boolean>(false);
  const [page, setPage] = React.useState<number>(0);
  const [offset, setOffset] = React.useState<number>(10);
  const [sort, setSort] = React.useState<[Sort, number]>([Sort.region, 1]);
  const [query, setQuery] = React.useState<string>("");

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleRequestSort = (property: Sort) => {
    if (sort[0] !== property) {
      setSort([property, sort[1]]);
    } else {
      setSort([property, -sort[1]]);
    }
    setPage(0);
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setOffset(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setQuery(e.target.value);
    setPage(0);
  };

  const { isLoading, data, error } = useQuery({
    queryKey: ["reports", page, offset, sort, query],
    queryFn: () => getReports(offset, offset * page, query, sort[0], sort[1]),
    staleTime: 5000,
  });

  return (
    <>
      <main>
        <Box sx={{ p: 1, display: "flex", justifyContent: "space-between" }}>
          <TextField
            label="Поиск"
            id="outlined-size-small"
            size="small"
            onChange={handleChange}
          />
          <Button variant="contained" sx={{ mr: 1 }} onClick={handleOpen}>
            Добавить отчет
          </Button>
        </Box>
        <Paper>
          <TableContainer>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell align="center">
                    <TableSortLabel
                      active={sort[0] === Sort.region}
                      direction={sort[1] === 1 ? "asc" : "desc"}
                      onClick={() => handleRequestSort(Sort.region)}
                    >
                      Федеральный округ
                    </TableSortLabel>
                  </TableCell>
                  <TableCell align="center">
                    <TableSortLabel
                      active={sort[0] === Sort.city}
                      direction={sort[1] === 1 ? "asc" : "desc"}
                      onClick={() => handleRequestSort(Sort.city)}
                    >
                      Место проведения контроля
                    </TableSortLabel>
                  </TableCell>
                  <TableCell align="center">
                    <TableSortLabel
                      active={sort[0] === Sort.start_date}
                      direction={sort[1] === 1 ? "asc" : "desc"}
                      onClick={() => handleRequestSort(Sort.start_date)}
                    >
                      Дата начала
                    </TableSortLabel>
                  </TableCell>
                  <TableCell align="center">
                    <TableSortLabel
                      active={sort[0] === Sort.end_date}
                      direction={sort[1] === 1 ? "asc" : "desc"}
                      onClick={() => handleRequestSort(Sort.end_date)}
                    >
                      Дата конца
                    </TableSortLabel>
                  </TableCell>
                  <TableCell align="center">Просмотр отчета</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data?.results.map((report) => (
                  <TableRow key={report.id}>
                    <TableCell scope="row" align="center">
                      {report.region}
                    </TableCell>
                    <TableCell align="center">{report.city}</TableCell>
                    <TableCell align="center">{report.start_date}</TableCell>
                    <TableCell align="center">{report.end_date}</TableCell>
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
          <TablePagination
            labelRowsPerPage="Кол-во строк на странице:"
            rowsPerPageOptions={[5, 10, 15]}
            component="div"
            count={data?.count || 0}
            rowsPerPage={data?.count ? offset : 0}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Paper>
      </main>
      <AddReportForm open={open} handleClose={handleClose} />
    </>
  );
}
