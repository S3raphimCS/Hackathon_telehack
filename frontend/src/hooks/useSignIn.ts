"use client";

import { saveTokens, signIn } from "@/services/users";
import { IUserSignIn } from "@/types/users";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

export function useSignIn() {
  const router = useRouter();

  const { mutate: signInMutation } = useMutation({
    mutationFn: (user: IUserSignIn) => signIn(user),
    onSuccess: (data) => {
      saveTokens(data);
      router.push("/");
    },
  });

  return signInMutation;
}
