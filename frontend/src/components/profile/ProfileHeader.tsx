import Link from "next/link";
import { Avatar } from "@/components/ui/Avatar";
import { Icon } from "@/components/ui/Icon";
import { formatMonthYear } from "@/lib/dates";
import type { MeUser } from "@/lib/types";

export function ProfileHeader({ user }: { user: MeUser }) {
  return (
    <header className="flex items-center gap-4 border-b-2 border-border pb-6">
      <Avatar name={user.display_name} color={user.avatar_color} size="lg" />
      <div className="min-w-0 flex-1">
        <h1 className="truncate text-3xl font-extrabold">{user.display_name}</h1>
        <p className="text-text-muted">@{user.username}</p>
        <p>Joined {formatMonthYear(user.joined_at)}</p>
      </div>
      <Link
        href="/settings"
        aria-label="Edit profile"
        className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border-2 border-b-4 border-border text-text-muted hover:bg-surface-subtle"
      >
        <Icon name="pencil" className="h-6 w-6" />
      </Link>
    </header>
  );
}
