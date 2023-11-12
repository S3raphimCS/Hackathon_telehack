import { IReportUpload } from "@/types/reports";
import { getAccessToken } from "./users";

export function getReports() {}

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
  if (!response.ok) throw new Error("error");
  return response.json();
}
