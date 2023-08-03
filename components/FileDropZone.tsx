import React, { useState } from "react";
import styled from "@emotion/styled";
import Paper from "@mui/material/Paper";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { Image } from "@mui/icons-material";
import { useTheme } from "@mui/material";

export default function FileDropZone({
  onFilesAdded,
}: {
  onFilesAdded: (f: File) => void;
}) {
  const [highlight, setHighlight] = useState(false);
  const [fileName, setFileName] = useState("");
  const theme = useTheme();

  const FileDropZoneContainer = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
    height: 200px;
    width: 100%;
    border: 2px dashed ${theme.palette.info.main};
    cursor: pointer;
  `;

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setHighlight(true);
  };

  const handleDragLeave = () => {
    setHighlight(false);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setHighlight(false);

    onFilesAdded(event.dataTransfer.files[0]);
    setFileName(event.dataTransfer.files[0].name);
  };

  return (
    <FileDropZoneContainer
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      style={{
        borderColor: highlight
          ? theme.palette.text.primary
          : theme.palette.text.secondary,
      }}
    >
      <Paper
        elevation={0}
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          background: theme.palette.background.paper,
        }}
      >
        {fileName ? (
          // eslint-disable-next-line jsx-a11y/alt-text
          <Image fontSize="large" />
        ) : (
          <CloudUploadIcon fontSize="large" />
        )}
        <p>{fileName == "" ? "Drag and drop 1 PDF file here" : fileName}</p>
      </Paper>
    </FileDropZoneContainer>
  );
}
