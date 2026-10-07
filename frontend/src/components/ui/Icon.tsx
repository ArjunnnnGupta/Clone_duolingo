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
  notebook:
    "M6 3h12a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zm2 4v2h8V7zm0 4v2h8v-2zm0 4v2h5v-2z",
} as const;

export type IconName = keyof typeof ICON_PATHS;

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
