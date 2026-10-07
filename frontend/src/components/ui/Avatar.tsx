import { getAvatarColorClasses } from "@/lib/avatarColors";

const SIZE_CLASSES = {
  sm: "h-10 w-10 text-lg",
  lg: "h-24 w-24 text-5xl",
} as const;

interface AvatarProps {
  name: string;
  // A colour token name from the server (e.g. "green").
  color: string;
  size?: keyof typeof SIZE_CLASSES;
}

// Coloured circle with the name's initial; there is no avatar upload.
export function Avatar({ name, color, size = "sm" }: AvatarProps) {
  return (
    <span
      aria-hidden="true"
      className={`flex shrink-0 items-center justify-center rounded-full font-extrabold text-on-color ${getAvatarColorClasses(color).fill} ${SIZE_CLASSES[size]}`}
    >
      {name.trim().charAt(0).toUpperCase()}
    </span>
  );
}
