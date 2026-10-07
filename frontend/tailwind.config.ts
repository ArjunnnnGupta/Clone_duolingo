import type { Config } from "tailwindcss";

// Each brand colour pairs a main fill with a darker "shade" used for the 3D bottom edge.
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        green: { DEFAULT: "#58CC02", shade: "#58A700" },
        blue: { DEFAULT: "#1CB0F6", shade: "#1899D6" },
        red: { DEFAULT: "#FF4B4B", shade: "#EA2B2B" },
        orange: { DEFAULT: "#FF9600", shade: "#CD7900" },
        gold: { DEFAULT: "#FFC800", shade: "#E5B400" },
        purple: { DEFAULT: "#CE82FF", shade: "#A568CC" },
        text: { DEFAULT: "#4B4B4B", muted: "#777777", subtle: "#AFAFAF" },
        border: "#E5E5E5",
        surface: { DEFAULT: "#FFFFFF", subtle: "#F7F7F7" },
        correct: { bg: "#D7FFB8", text: "#58A700" },
        wrong: { bg: "#FFDFE0", text: "#EA2B2B" },
      },
      // 3D "thickness" under each path node; hex repeats the colour shades above because
      // box-shadow cannot reference a Tailwind colour token.
      boxShadow: {
        "node-green": "0 8px 0 #58A700",
        "node-blue": "0 8px 0 #1899D6",
        "node-purple": "0 8px 0 #A568CC",
        "node-gold": "0 8px 0 #E5B400",
        "node-locked": "0 8px 0 #AFAFAF",
      },
      fontFamily: {
        sans: ["var(--font-nunito)", "system-ui", "sans-serif"],
      },
    },
  },
};

export default config;
