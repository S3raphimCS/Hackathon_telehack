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

export default function Home() {
  const [open, setOpen] = React.useState<boolean>(false);

  const handleOpen = () => {
    setOpen(true);
  }

  const handleClose = () => {
    setOpen(false);
  }

  useUser();

  return (
    <>
      <main>
        <Box sx={{ p: 1 }}>
          <Button variant="contained" sx={{ mr: 1 }} onClick={handleOpen}>
            Добавить отчет
          </Button>
          <Button variant="contained">Обновить страницу</Button>
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
              <TableRow>
                <TableCell scope="row" align="center">
                  УФО
                </TableCell>
                <TableCell align="center">г. Екатеринбург</TableCell>
                <TableCell align="center">01.01.2023 - 03.01.2023</TableCell>
                <TableCell align="center">
                  <Button LinkComponent={Link} href="#">
                    Просмотреть
                  </Button>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </main>
      <AddReportForm open={open} handleClose={handleClose}/>
    </>
  );
}
