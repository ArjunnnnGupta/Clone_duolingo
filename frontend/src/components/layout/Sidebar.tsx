import { NAV_ITEMS } from "@/lib/navItems";
import { NavItem } from "./NavItem";

// Icon-only from 768px, full labels from 1024px; replaced by MobileTabBar below 768px.
export function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 hidden w-[88px] flex-col gap-2 border-r-2 border-border px-3 py-6 md:flex lg:w-64">
      <p className="mb-6 hidden px-3 text-3xl font-extrabold tracking-tight text-green lg:block">
        lingoleap
      </p>
      <nav className="flex flex-col gap-2">
        {NAV_ITEMS.map((item) => (
          <NavItem key={item.href} {...item} />
        ))}
      </nav>
    </aside>
  );
}
