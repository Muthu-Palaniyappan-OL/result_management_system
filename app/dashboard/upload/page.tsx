"use client";

import FileDropZone from "@/components/FileDropZone";
import {
  Box,
  Button,
  LinearProgress,
  Typography,
  useTheme,
} from "@mui/material";
import { useState } from "react";
import { processPdfDocument } from "./action";

export default function Upload() {
  const [file, setFile] = useState<File | undefined>();
  const [uploading, setUploading] = useState<boolean>(false);
  const [error, setError] = useState("");
  const theme = useTheme();

  async function uploadFile() {
    if (file == undefined) return setError("No File");
    setError("");
    setUploading(true);
    await processPdfDocument(Buffer.from(await file.arrayBuffer()).buffer);
  }

  return (
    <Box>
      <FileDropZone onFilesAdded={(f) => setFile(f)} />
      <Box marginTop={3} display={"flex"} gap={2}>
        <Button variant="contained" onClick={() => uploadFile()}>
          Upload
        </Button>
      </Box>
      {uploading ? (
        <Box paddingY={3}>
          <LinearProgress />
        </Box>
      ) : (
        <></>
      )}
      {error ? (
        <Box
          marginTop={3}
          padding={3}
          bgcolor={theme.palette.common.black}
          color={theme.palette.common.white}
        >
          <Typography
            variant="h6"
            sx={{ textDecoration: "underline" }}
            paddingBottom={3}
          >
            Log
          </Typography>
          {error}
        </Box>
      ) : (
        <></>
      )}
    </Box>
  );
}
