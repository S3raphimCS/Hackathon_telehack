"use client";

import { IReportUpload, IReports, Report } from "@/types/reports";
import { getAccessToken } from "./users";
import { IError } from "@/types/errors";

export async function getReports(
  limit: number,
  offset: number,
  query: string,
  sort: string,
  ascOrDesc: number
): Promise<IReports | undefined> {
  const response = await fetch(
    `http://localhost:8000/api/v1/metrics/report/search/?query=${query}&sort=${sort},${ascOrDesc}&limit=${limit}&offset=${offset}`,
    {
      headers: {
        Authorization: `Bearer ${getAccessToken()}`,
      },
    }
  );

  if (response.status === 403) {
    window.location.replace("/signin");
    return;
  }

  if (!response.ok) throw new Error("error");
  return response.json();
}

export async function uploadReport(data: IReportUpload): Promise<any> {
  const formData = new FormData();
  formData.append("file", data.files[0]);
  const response = await fetch(
    "http://localhost:8000/api/v1/metrics/report/upload/",
    {
      method: "POST",
      body: formData,
      headers: {
        Authorization: `Bearer ${getAccessToken()}`,
      },
    }
  );
  if (response.status === 403) {
    window.location.replace("/signin");
    return;
  }

  const json = await response.json();

  if (!response.ok) {
    const error = json as IError;
    throw new Error(error.error);
  }
  return json;
}

export async function getReport(id: number): Promise<Report | undefined> {
  const response = await fetch(
    `http://localhost:8000/api/v1/metrics/report/${id}`,
    {
      headers: {
        Authorization: `Bearer ${getAccessToken()}`,
      },
    }
  );

  if (response.status === 403) {
    window.location.replace("/signin");
    return;
  }

  if (!response.ok) throw new Error("error");
  return response.json();
}

export async function editReport(id: number, report: Report): Promise<any> {
  const start_date = report.start_date as Date;
  report.start_date = start_date.toISOString().split("T")[0];

  const end_date = report.end_date as Date;
  report.end_date = end_date.toISOString().split("T")[0];

  const response = await fetch(
    `http://127.0.0.1:8000/api/v1/metrics/report/${id}/edit`,
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${getAccessToken()}`,
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(report),
    }
  );

  const json = await response.json();

  if (response.status === 403) {
    window.location.replace("/signin");
    return;
  }

  if (!response.ok){
    const error = json as IError;
    throw new Error(error.detail);
  } 
  return json;
}
