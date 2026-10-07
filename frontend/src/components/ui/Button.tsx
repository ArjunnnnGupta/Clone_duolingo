import type { ButtonHTMLAttributes } from "react";

// "white" stays white in both themes and leaves the text colour to the caller, so it can match
// the coloured card it sits on.
const VARIANT_CLASSES = {
  primary: "border-green-shade bg-green text-on-color",
  secondary: "border-blue-shade bg-blue text-on-color",
  danger: "border-red-shade bg-red text-on-color",
  white: "border-border bg-on-color",
  ghost: "border-transparent bg-transparent text-red hover:bg-surface-subtle",
  locked: "border-border bg-border text-text-subtle",
} as const;

const BASE_CLASSES =
  "h-[50px] w-full rounded-2xl border-b-4 text-[15px] font-extrabold uppercase tracking-[0.8px] hover:brightness-105";

// Pressing drops the button onto its 4px bottom edge, so it looks physically pushed in.
const PRESS_CLASSES = "active:translate-y-1 active:border-b-0";

// Disabled buttons neither brighten nor press.
const DISABLED_CLASSES =
  "disabled:cursor-not-allowed disabled:hover:brightness-100 disabled:active:translate-y-0 disabled:active:border-b-4";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof VARIANT_CLASSES;
}

export function Button({
  variant = "primary",
  type = "button",
  className = "",
  ...buttonProps
}: ButtonProps) {
  return (
    <button
      type={type}
      className={`${BASE_CLASSES} ${PRESS_CLASSES} ${DISABLED_CLASSES} ${VARIANT_CLASSES[variant]} ${className}`}
      {...buttonProps}
    />
  );
}
