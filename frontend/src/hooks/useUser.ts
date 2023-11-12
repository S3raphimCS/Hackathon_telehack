"use client";

import { getUser, removeTokens } from "@/services/users";
import { IUser } from "@/types/users";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

interface IUseUser {
  user: IUser | null;
}

export function useUser(): IUseUser {
  const router = useRouter();

  const { data: user, isLoading} = useQuery<IUser | null>({
    queryKey: ["user"],
    queryFn: getUser,
    refetchOnMount: true,
    retry: false,
  });

  useEffect(() => {
    console.log(user)
    if (!isLoading && !user) {
      removeTokens();
      router.push("/signin");
    }
  }, [isLoading]);

  return {
    user: user ?? null,
  };
}
