import express from "express";
import uploadRouter from "./routes/upload";

const app = express();
const PORT = process.env.PORT || 8080;

app.use("/upload", uploadRouter);

app.listen(PORT, () => console.log(`Listening in port ${PORT}`));
