"use client";

import {
  Avatar,
  Box,
  Container,
  TextField,
  Button,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { login } from "./action";
import { useRouter } from "next/navigation";

export default function Home() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  async function submit() {
    const response = await login(username, password);
    console.log(response);

    if (response == "Success") {
      router.push("/dashboard");
    }
  }

  return (
    <Container
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "80vh",
      }}
    >
      <Box display={"flex"} maxWidth={800} flexDirection={"column"} gap={2}>
        <Box display={"flex"} maxWidth={800} flexDirection={"row"} gap={2}>
          <Avatar />
          <Typography variant="h6">Sign In</Typography>
        </Box>
        <TextField
          label="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <TextField
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button variant="contained" onClick={() => submit()}>
          Login
        </Button>
      </Box>
    </Container>
  );
}
