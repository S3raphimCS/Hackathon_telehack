"use client";

import React from "react";
import Button from "@mui/material/Button";
import Input from "@mui/material/Input";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { useForm } from "react-hook-form";
import { uploadReport } from "@/services/reports";
import { IReportUpload } from "@/types/reports";

export default function AddReportForm({
  open,
  handleClose,
}: {
  open: boolean;
  handleClose: () => void;
}) {
  const { register, handleSubmit, watch, reset } = useForm<IReportUpload>();
  const files = watch("files");

  const onSubmit = (data: IReportUpload) => {
    try {
      uploadReport(data);
    } catch (e) {
      console.log(e);
    }
  };

  const handleCloseWithReset = () => {
    reset();
    handleClose();
  };

  return (
    <Modal open={open} onClose={handleCloseWithReset}>
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: 400,
          bgcolor: "background.paper",
          boxShadow: 24,
          p: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <form onSubmit={handleSubmit(onSubmit)}>
          <Button component="label" variant="contained">
            Выбрать файл
            <Input
              type="file"
              sx={{
                clip: "rect(0 0 0 0)",
                clipPath: "inset(50%)",
                height: 1,
                overflow: "hidden",
                position: "absolute",
                bottom: 0,
                left: 0,
                whiteSpace: "nowrap",
                width: 1,
              }}
              {...register("files")}
            />
          </Button>
          <Typography noWrap sx={{ m: 1 }}>
            {files?.[0]?.name}
          </Typography>
          <Button
            type="submit"
            variant="contained"
            startIcon={<CloudUploadIcon />}
            sx={{ margin: "0 auto" }}
          >
            Загрузить отчет
          </Button>
        </form>
      </Box>
    </Modal>
  );
}