import type { SVGProps } from "react";

// Original single-path glyphs on a 24px grid; colour comes from the parent's text colour.
const ICON_PATHS = {
  star: "M12 2l2.9 6.3 6.9.8-5.1 4.7 1.4 6.8L12 17.3l-6.1 3.3 1.4-6.8-5.1-4.7 6.9-.8z",
  check: "M9.5 17.2 4.8 12.5l1.9-1.9 2.8 2.8 7.8-7.8 1.9 1.9z",
  flame: "M12 2c1 3.5 5 6 5 11a5 5 0 0 1-10 0c0-2 1-3.5 2-4.5.2 1.2.8 2 1.6 2.3C10 8 10.5 4.5 12 2z",
  bolt: "M13 2 4 14h6l-1 8 9-12h-6z",
  gem: "M6 3h12l4 6-10 12L2 9z",
  heart: "M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z",
  home: "M12 3 2 12h3v8h5v-5h4v5h5v-8h3z",
  shield: "M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z",
  chest: "M3 8a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v3H3zm0 4h7v2h4v-2h7v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z",
  shop: "M4 4h16l2 5a3 3 0 0 1-5 1.5A3 3 0 0 1 12 12a3 3 0 0 1-5-1.5A3 3 0 0 1 2 9zm1 9h14v7H5z",
  user: "M12 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10zm-8 9a8 8 0 0 1 16 0z",
  more: "M5 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4z",
  close: "M6.4 5 12 10.6 17.6 5 19 6.4 13.4 12 19 17.6 17.6 19 12 13.4 6.4 19 5 17.6 10.6 12 5 6.4z",
  pencil: "M3 17.3V21h3.7L17.8 9.9l-3.7-3.7zM20.7 7a1 1 0 0 0 0-1.4l-2.3-2.3a1 1 0 0 0-1.4 0l-1.8 1.8 3.7 3.7z",
  footprints:
    "M8 3C6 3 5 5 5 8s1 5 3 5 3-2 3-5-1-5-3-5zM7 15h4v3a2 2 0 0 1-4 0zM16 3c-2 0-3 2-3 5s1 5 3 5 3-2 3-5-1-5-3-5zM15 15h4v3a2 2 0 0 1-4 0z",
  book: "M6 3h11a2 2 0 0 1 2 2v13a1 1 0 0 1-1 1H7a2 2 0 0 0 0 2h11v1H7a3 3 0 0 1-3-3V5a2 2 0 0 1 2-2zm1 3v2h8V6z",
  "graduation-cap":
    "M12 3 1 9l11 6 9-4.9V17h2V9zM5 13.2V17c0 1.7 3.1 3 7 3s7-1.3 7-3v-3.8l-7 3.8z",
  target:
    "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM12 5a7 7 0 1 0 0 14 7 7 0 0 0 0-14zM12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM12 11a1 1 0 1 0 0 2 1 1 0 0 0 0-2z",
  notebook:
    "M6 3h12a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zm2 4v2h8V7zm0 4v2h8v-2zm0 4v2h5v-2z",
} as const;

export type IconName = keyof typeof ICON_PATHS;

// Icon names that arrive as strings from the server (e.g. achievements) fall back to a star.
export function toIconName(name: string): IconName {
  return name in ICON_PATHS ? (name as IconName) : "star";
}

interface IconProps extends SVGProps<SVGSVGElement> {
  name: IconName;
}

export function Icon({ name, ...svgProps }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" {...svgProps}>
      <path fillRule="evenodd" d={ICON_PATHS[name]} />
    </svg>
  );
}
