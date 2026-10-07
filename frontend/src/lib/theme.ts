// Light by default; a learner who picks dark in Settings gets it saved in localStorage, and the
// inline script in app/layout.tsx applies it before the first paint (no flash).
export type Theme = "light" | "dark";

export const THEME_STORAGE_KEY = "theme";
const THEME_CHANGE_EVENT = "themechange";

export const APPLY_SAVED_THEME_SCRIPT = `(function(){try{var t=localStorage.getItem("${THEME_STORAGE_KEY}");if(t==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}})()`;

export function readTheme(): Theme {
  return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
}

export function applyTheme(theme: Theme): void {
  document.documentElement.setAttribute("data-theme", theme);
  try {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  } catch {
    // Storage can be unavailable (private mode); the theme still applies for this visit.
  }
  window.dispatchEvent(new Event(THEME_CHANGE_EVENT));
}

export function subscribeToTheme(onChange: () => void): () => void {
  window.addEventListener(THEME_CHANGE_EVENT, onChange);
  return () => window.removeEventListener(THEME_CHANGE_EVENT, onChange);
}
