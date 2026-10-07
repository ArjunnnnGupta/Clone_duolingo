// Original placeholder character; Phase 9 replaces it with the full set of poses.
export function Mascot({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 64 64" className={className} aria-hidden="true">
      <ellipse cx="32" cy="58" rx="20" ry="5" className="fill-border" />
      <path d="M12 52C8 30 18 10 32 10s24 20 20 42z" className="fill-purple" />
      <circle cx="24" cy="30" r="7" className="fill-surface" />
      <circle cx="40" cy="30" r="7" className="fill-surface" />
      <circle cx="25" cy="31" r="3.5" className="fill-text" />
      <circle cx="41" cy="31" r="3.5" className="fill-text" />
      <path
        d="M26 42q6 6 12 0"
        fill="none"
        strokeWidth="3"
        strokeLinecap="round"
        className="stroke-purple-shade"
      />
    </svg>
  );
}
