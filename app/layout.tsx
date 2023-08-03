"use client";

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "@fontsource/roboto";
import {
  CssBaseline,
  ThemeProvider,
  createTheme,
  useMediaQuery,
} from "@mui/material";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Result Management System",
  description: "",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const preference = useMediaQuery("(prefers-color-scheme: dark)");
  const theme = createTheme({
    palette: {
      mode: preference ? "dark" : "light",
    },
  });

  return (
    <html lang="en">
      <body className={inter.className} style={{ fontFamily: "Roboto" }}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
