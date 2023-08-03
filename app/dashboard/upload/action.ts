"use server";

import globalConfig from "@/app/global.config";
import { exec } from "child_process";
import { join } from "path";

export async function processPdfDocument(buffer: ArrayBufferLike) {
  console.log(buffer);

  exec(join("./main.exe"), (err, out, outErr) => {
    if (err) {
      console.log(err);
    }
    console.log(out, outErr);
    return "Success";
  });
}
