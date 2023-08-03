"use client";

import {
  Box,
  CssBaseline,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  useTheme,
} from "@mui/material";
import Link from "next/link";
import { logout } from "../action";
import HomeIcon from "@mui/icons-material/Home";
import UploadIcon from "@mui/icons-material/Upload";
import LogoutIcon from "@mui/icons-material/Logout";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const theme = useTheme();

  return (
    <Box flex={"row"} display={"flex"}>
      <CssBaseline />
      <Drawer
        sx={{
          display: "block",
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            position: "relative",
            height: "100vh",
          },
        }}
        anchor="left"
        variant="permanent"
        open
      >
        <List>
          <ListItem disablePadding>
            <Link
              href={"/dashboard"}
              style={{
                textDecoration: "none",
                color: theme.palette.text.primary,
                width: "100%",
              }}
            >
              <ListItemButton sx={{ display: "flex", gap: 1 }}>
                <HomeIcon />
                Home
              </ListItemButton>
            </Link>
          </ListItem>
          <ListItem disablePadding>
            <Link
              href={"/dashboard/upload"}
              style={{
                textDecoration: "none",
                color: theme.palette.text.primary,
              }}
            >
              <ListItemButton sx={{ display: "flex", gap: 1 }}>
                <UploadIcon />
                Upload
              </ListItemButton>
            </Link>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton
              sx={{ display: "flex", gap: 1 }}
              onClick={async () => {
                await logout();
                window.location.href = "/";
              }}
            >
              <LogoutIcon />
              Logout
            </ListItemButton>
          </ListItem>
        </List>
      </Drawer>
      <Box sx={{ flexGrow: 1, padding: 2 }}>{children}</Box>
    </Box>
  );
}
