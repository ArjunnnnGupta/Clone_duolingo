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
  // Skill glyphs (the `icon` names the server sends for each skill).
  wave: "M8 21c-2.8 0-5-2.2-5-5v-4.5a1.5 1.5 0 0 1 3 0V13h1V5.5a1.5 1.5 0 0 1 3 0V12h1V4a1.5 1.5 0 0 1 3 0v8h1V5.5a1.5 1.5 0 0 1 3 0V15c0 3.3-2.7 6-6 6z",
  apple:
    "M12 7c-1-1.5-3-2-4.5-1.5C5 6.3 3.5 9 4.3 12.6 5 16 7.5 20 9.5 20c1 0 1.5-.6 2.5-.6s1.5.6 2.5.6c2 0 4.5-4 5.2-7.4C20.5 9 19 6.3 16.5 5.5 15 5 13 5.5 12 7zm0-1c0-2 1.2-3.5 3-4-.1 2-1.2 3.6-3 4z",
  family:
    "M7 6a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zm10 0a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zm-5 6a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM2 19a5 5 0 0 1 9-3 4 4 0 0 0-3 3zm20 0a5 5 0 0 0-9-3 4 4 0 0 1 3 3zM8 21a4 4 0 0 1 8 0z",
  people:
    "M8 4a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm8 1a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM2 20a6 6 0 0 1 12 0zm12.5 0a7.5 7.5 0 0 0-2-4.8A5 5 0 0 1 22 20z",
  building: "M4 21V5l8-3v19zm10 0V9l6 2v10zM6 7h2v2H6zm0 4h2v2H6zm0 4h2v2H6zm10 0h2v2h-2zm0-4h2v2h-2z",
  plane:
    "M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z",
  signpost: "M11 2h2v2h6l3 3-3 3h-6v12h-2V10H5V4h6z",
  clock: "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 5h-2v6l5 3 1-1.7-4-2.3z",
  sunrise:
    "M12 9a6 6 0 0 1 6 6H6a6 6 0 0 1 6-6zM2 17h20v2H2zm9-14h2v4h-2zM4.2 6.6l1.4-1.4 2.1 2.1-1.4 1.4zm14.2-1.4 1.4 1.4-2.1 2.1-1.4-1.4z",
  cloud: "M7 19a5 5 0 0 1-.6-10A6 6 0 0 1 18 8.5 5 5 0 0 1 17.5 19z",
  palette:
    "M12 2C6.5 2 2 6 2 11c0 4 3 7 6 7h1.5a1.5 1.5 0 0 1 1.1 2.5 1.5 1.5 0 0 0 1.1 1.5H12c5.5 0 10-4.5 10-10S17.5 2 12 2zM7 12a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm3-4a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm3 4a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z",
  smile:
    "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM8.5 8a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zm7 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zM7 14h10a5 5 0 0 1-10 0z",
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
