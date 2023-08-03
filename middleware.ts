import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { jwtVerify } from "jose";
import globalConfig from "./app/global.config";

export const runtime = "nodejs";

export async function middleware(request: NextRequest) {
  try {
    const decoded = await jwtVerify(
      request.cookies.get("jwt")?.value || "",
      globalConfig.JWT_SECRET
    );
  } catch (e: any) {
    console.log(e);
    return NextResponse.redirect(new URL("/", request.url));
  }
}

// See "Matching Paths" below to learn more
export const config = {
  matcher: "/dashboard/:path*",
};
