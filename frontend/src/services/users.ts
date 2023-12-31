"use client";

import { ITokens, IUser, IUserSignIn } from "@/types/users";
import { IError } from "@/types/errors";

export async function signIn({
  email,
  password,
}: IUserSignIn): Promise<ITokens | Error> {
  const formData = new FormData();
  formData.append("email", email);
  formData.append("password", password);

  const response = await fetch("http://localhost:8000/api/v1/auth/login/", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    const error = data as IError;
    throw new Error(error.detail);
  }

  return data;
}

export async function getUser(): Promise<IUser | null> {
  const response = await fetch(`http://localhost:8000/api/v1/users/me/`, {
    headers: {
      Authorization: `Bearer ${getAccessToken()}`,
    },
  });
  if (!response.ok) throw new Error("Failed on get user request");

  return response.json();
}

export function saveTokens(tokens: ITokens): void {
  localStorage.setItem("accessToken", tokens.access);
  localStorage.setItem("refreshToken", tokens.refresh);
}

export function getAccessToken(): string {
  return localStorage.getItem("accessToken") || "";
}

export function removeTokens(): void {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
}
