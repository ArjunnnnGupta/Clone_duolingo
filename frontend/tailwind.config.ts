import type { Config } from "tailwindcss";

// Every colour is a CSS variable defined in src/app/globals.css, once for the light theme and
// once for [data-theme="dark"]. Components only ever name the token, so switching theme swaps
// every colour without touching a component. Each brand colour pairs a main fill with a darker
// "shade" used for the 3D bottom edge.
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        green: { DEFAULT: "var(--c-green)", shade: "var(--c-green-shade)" },
        blue: { DEFAULT: "var(--c-blue)", shade: "var(--c-blue-shade)" },
        red: { DEFAULT: "var(--c-red)", shade: "var(--c-red-shade)" },
        orange: { DEFAULT: "var(--c-orange)", shade: "var(--c-orange-shade)" },
        gold: { DEFAULT: "var(--c-gold)", shade: "var(--c-gold-shade)" },
        purple: { DEFAULT: "var(--c-purple)", shade: "var(--c-purple-shade)" },
        text: {
          DEFAULT: "var(--c-text)",
          muted: "var(--c-text-muted)",
          subtle: "var(--c-text-subtle)",
        },
        border: "var(--c-border)",
        surface: { DEFAULT: "var(--c-surface)", subtle: "var(--c-surface-subtle)" },
        // Text and marks drawn on a coloured fill (buttons, banners, nodes): white in both themes.
        "on-color": "var(--c-on-color)",
        // Modal backdrop.
        scrim: "var(--c-scrim)",
        correct: { bg: "var(--c-correct-bg)", text: "var(--c-correct-text)" },
        wrong: { bg: "var(--c-wrong-bg)", text: "var(--c-wrong-text)" },
        // The original cat mascot: a deliberately neon red, distinct from the error/heart red.
        // Fixed values: the cat looks the same in both themes.
        mascot: { DEFAULT: "#FF1744", shade: "#C4001D", light: "#FF7A8F", ink: "#3C3C3C" },
      },
      // 3D "thickness" under each path node, drawn in the matching shade.
      boxShadow: {
        "node-green": "0 8px 0 var(--c-green-shade)",
        "node-blue": "0 8px 0 var(--c-blue-shade)",
        "node-purple": "0 8px 0 var(--c-purple-shade)",
        "node-gold": "0 8px 0 var(--c-gold-shade)",
        "node-locked": "0 8px 0 var(--c-node-locked-edge)",
      },
      fontFamily: {
        sans: ["var(--font-nunito)", "system-ui", "sans-serif"],
      },
    },
  },
};

export default config;
