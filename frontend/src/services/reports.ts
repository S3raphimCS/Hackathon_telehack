"use client";

import { IReportUpload, IReports, Report } from "@/types/reports";
import { getAccessToken } from "./users";

export async function getReports(
  limit: number,
  offset: number
): Promise<IReports | undefined> {
  const response = await fetch(
    `http://localhost:8000/api/v1/metrics/reports/?limit=${limit}&offset=${offset}`,
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

  if (!response.ok) throw new Error("error");
  return response.json();
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
  const response = await fetch(
    `http://127.0.0.1:8000/api/v1/metrics/report/${id}/edit`,
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${getAccessToken()}`,
      },
      body: JSON.stringify(report),
    }
  );

  if (response.status === 403) {
    window.location.replace("/signin");
    return;
  }

  if (!response.ok) throw new Error("error");
    return response.json();
}
