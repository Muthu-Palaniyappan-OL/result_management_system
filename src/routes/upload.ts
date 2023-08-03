/// <reference path="../types/express.d.ts" />

import multer from "multer";
import { Router } from "express";
import { handleError } from "../utils/error";
import { spawn } from "child_process";

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

const uploadRouter = Router();

uploadRouter.post("/", upload.single("file"), (req, res) => {
  try {
    if (req.file == undefined) throw new Error("File is not sent");
    const process = spawn(__dirname + "/main.exe");
    process.stdin.write(req.file.buffer);
    process.stdin.end();
    let output = "";
    process.stdout.on("data", (d) => (output += String(d)));
    process.on("close", () => {
      return res.contentType("json").send(output).end();
    });
  } catch (e: any) {
    return handleError(res, String(e));
  }
});

export default uploadRouter;
