export type MascotPose = "idle" | "happy" | "sad";

interface MascotProps {
  className?: string;
  pose?: MascotPose;
}

// Original neon-red cat (never Duolingo's owl): one chunky head-and-body shape, big eyes, and a
// face that changes with the pose. Colours come from the mascot tokens.
export function Mascot({ className = "", pose = "idle" }: MascotProps) {
  return (
    <svg viewBox="0 0 120 120" className={className} aria-hidden="true">
      <ellipse cx="60" cy="112" rx="34" ry="5" className="fill-border" />
      <CatBody />
      <CatEyes pose={pose} />
      <CatMouth pose={pose} />
    </svg>
  );
}

function CatBody() {
  return (
    <g>
      <path d="M22 46 28 10 54 30Z" strokeLinejoin="round" strokeWidth="6" className="fill-mascot stroke-mascot" />
      <path d="M98 46 92 10 66 30Z" strokeLinejoin="round" strokeWidth="6" className="fill-mascot stroke-mascot" />
      <path d="M30 34 32 20 44 30Z" className="fill-mascot-light" />
      <path d="M90 34 88 20 76 30Z" className="fill-mascot-light" />
      <rect x="16" y="24" width="88" height="84" rx="40" className="fill-mascot" />
      <ellipse cx="60" cy="90" rx="26" ry="16" className="fill-mascot-light" />
      <ellipse cx="44" cy="108" rx="10" ry="5" className="fill-mascot-shade" />
      <ellipse cx="76" cy="108" rx="10" ry="5" className="fill-mascot-shade" />
      <path d="M10 64h18M10 72l18-3M110 64H92M110 72l-18-3" strokeWidth="2.5" strokeLinecap="round" className="stroke-mascot-shade" />
    </g>
  );
}

function CatEyes({ pose }: { pose: MascotPose }) {
  // Happy eyes are bigger; sad pupils sit low and the brows tilt up in the middle.
  const radius = pose === "happy" ? 16 : 14;
  const pupilY = pose === "sad" ? 62 : 57;
  return (
    <g>
      {[42, 78].map((cx) => (
        <g key={cx}>
          <circle cx={cx} cy="56" r={radius} className="fill-on-color" />
          <circle cx={cx + 2} cy={pupilY} r={pose === "happy" ? 9 : 8} className="fill-mascot-ink" />
          <circle cx={cx + 5} cy={pupilY - 4} r="3" className="fill-on-color" />
        </g>
      ))}
      {pose === "sad" && (
        <>
          <path d="M28 40 52 34M92 40 68 34" strokeWidth="4" strokeLinecap="round" className="stroke-mascot-shade" />
          <path d="M30 72q-3 6 0 9q3-3 0-9Z" className="fill-blue" />
        </>
      )}
    </g>
  );
}

function CatMouth({ pose }: { pose: MascotPose }) {
  return (
    <g>
      <path d="M56 70h8l-4 4Z" strokeLinejoin="round" strokeWidth="2" className="fill-mascot-shade stroke-mascot-shade" />
      {pose === "idle" && (
        <path d="M52 77q4 4 8 0q4 4 8 0" fill="none" strokeWidth="2.5" strokeLinecap="round" className="stroke-mascot-shade" />
      )}
      {pose === "happy" && (
        <>
          <path d="M48 76q12 16 24 0Z" className="fill-mascot-ink" />
          <path d="M53 81q7 5 14 0q-7 5-14 0Z" className="fill-mascot-light" />
        </>
      )}
      {pose === "sad" && (
        <path d="M52 82q8-7 16 0" fill="none" strokeWidth="2.5" strokeLinecap="round" className="stroke-mascot-shade" />
      )}
    </g>
  );
}
