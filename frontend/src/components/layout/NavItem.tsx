"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Icon } from "@/components/ui/Icon";
import type { NavItemConfig } from "@/lib/navItems";

export function NavItem({ href, label, icon }: NavItemConfig) {
  const isActive = usePathname().startsWith(href);
  const stateClasses = isActive
    ? "border-blue bg-blue/10 text-blue"
    : "border-transparent text-text-muted hover:bg-surface-subtle";

  return (
    <Link
      href={href}
      aria-current={isActive ? "page" : undefined}
      className={`flex items-center justify-center gap-4 rounded-xl border-2 px-3 py-3 text-[15px] font-extrabold uppercase tracking-[0.8px] lg:justify-start ${stateClasses}`}
    >
      <Icon name={icon} className="h-7 w-7 shrink-0" />
      <span className="hidden lg:inline">{label}</span>
    </Link>
  );
}
