// Tailwind only generates classes it sees whole, so each avatar colour token maps to literals.
export interface AvatarColorClasses {
  fill: string;
  text: string;
}

const AVATAR_COLOR_CLASSES: Record<string, AvatarColorClasses> = {
  green: { fill: "bg-green", text: "text-green" },
  blue: { fill: "bg-blue", text: "text-blue" },
  red: { fill: "bg-red", text: "text-red" },
  orange: { fill: "bg-orange", text: "text-orange" },
  gold: { fill: "bg-gold", text: "text-gold-shade" },
  purple: { fill: "bg-purple", text: "text-purple" },
};

export function getAvatarColorClasses(color: string): AvatarColorClasses {
  return AVATAR_COLOR_CLASSES[color] ?? AVATAR_COLOR_CLASSES.green;
}
