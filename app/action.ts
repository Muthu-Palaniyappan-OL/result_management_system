"use server";

import { cookies } from "next/headers";
import { SignJWT, jwtVerify } from "jose";
import globalConfig from "./global.config";

export async function login(username: string, password: string) {
  if (username == "admin" && password == "admin") {
    cookies().set(
      "jwt",
      await new SignJWT({ username: "admin" })
        .setProtectedHeader({ alg: "HS256" })
        .sign(globalConfig.JWT_SECRET)
    );
    return "Success";
  } else return "Wrong username or password";
}

export async function validLogin() {
  try {
    const cookie = cookies().get("jwt")?.value;
    if (cookie == undefined) return false;
    jwtVerify(cookie, globalConfig.JWT_SECRET);
    return true;
  } catch (e: any) {
    return false;
  }
}

export async function logout() {
  cookies().delete("jwt");
}
