import type { IconName } from "@/components/ui/Icon";

export interface NavItemConfig {
  href: string;
  label: string;
  icon: IconName;
}

export const NAV_ITEMS: NavItemConfig[] = [
  { href: "/learn", label: "Learn", icon: "home" },
  { href: "/leaderboard", label: "Leaderboards", icon: "shield" },
  { href: "/quests", label: "Quests", icon: "chest" },
  { href: "/shop", label: "Shop", icon: "shop" },
  { href: "/profile", label: "Profile", icon: "user" },
  { href: "/settings", label: "More", icon: "more" },
];
