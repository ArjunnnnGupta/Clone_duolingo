"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Icon } from "@/components/ui/Icon";
import { NAV_ITEMS } from "@/lib/navItems";

export function MobileTabBar() {
  const pathname = usePathname();

  return (
    <nav className="fixed inset-x-0 bottom-0 z-30 flex justify-around border-t-2 border-border bg-surface px-2 py-2 md:hidden">
      {NAV_ITEMS.map(({ href, label, icon }) => {
        const isActive = pathname.startsWith(href);
        const stateClasses = isActive
          ? "border-blue bg-blue/10 text-blue"
          : "border-transparent text-text-muted";
        return (
          <Link
            key={href}
            href={href}
            aria-label={label}
            aria-current={isActive ? "page" : undefined}
            className={`rounded-xl border-2 p-2 ${stateClasses}`}
          >
            <Icon name={icon} className="h-7 w-7" />
          </Link>
        );
      })}
    </nav>
  );
}
