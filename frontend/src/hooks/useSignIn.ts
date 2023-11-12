"use client";

import { saveTokens, signIn } from "@/services/users";
import { ITokens, IUserSignIn } from "@/types/users";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";

export function useSignIn() {
  const router = useRouter();

  const { mutate: signInMutation } = useMutation({
    mutationFn: (user: IUserSignIn) => signIn(user),
    onSuccess: (data) => {
      saveTokens(data as ITokens);
      router.push("/");
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });

  return signInMutation;
}
