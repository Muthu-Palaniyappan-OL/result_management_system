import { Response } from "express";

export function handleError(res: Response, errorMessage: string) {
  res.status(400);
  res.statusMessage = errorMessage;
  return res.end();
}
