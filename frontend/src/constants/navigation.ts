import {
  LayoutDashboard,
  PenSquare,
  ChartColumn,
  Route,
  Bot,
  User,
  Settings,
} from "lucide-react";

export const navigation = [
  {
    title: "Dashboard",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    title: "Practice",
    path: "/practice",
    icon: PenSquare,
  },
  {
    title: "Analytics",
    path: "/analytics",
    icon: ChartColumn,
  },
  {
    title: "Learning Path",
    path: "/learning-path",
    icon: Route,
  },
  {
    title: "AI Coach",
    path: "/ai-coach",
    icon: Bot,
  },
  {
    title: "Profile",
    path: "/profile",
    icon: User,
  },
  {
    title: "Settings",
    path: "/settings",
    icon: Settings,
  },
];