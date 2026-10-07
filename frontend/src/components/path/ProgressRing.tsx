const RING_SIZE_PX = 100;
const STROKE_WIDTH_PX = 6;
const RADIUS = (RING_SIZE_PX - STROKE_WIDTH_PX) / 2;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

interface ProgressRingProps {
  fraction: number;
  strokeClassName: string;
}

// Starts at 12 o'clock and fills clockwise.
export function ProgressRing({ fraction, strokeClassName }: ProgressRingProps) {
  const filledLength = CIRCUMFERENCE * Math.min(Math.max(fraction, 0), 1);
  const circleProps = {
    cx: RING_SIZE_PX / 2,
    cy: RING_SIZE_PX / 2,
    r: RADIUS,
    fill: "none",
    strokeWidth: STROKE_WIDTH_PX,
  };

  return (
    <svg
      width={RING_SIZE_PX}
      height={RING_SIZE_PX}
      className="absolute -rotate-90"
      aria-hidden="true"
    >
      <circle {...circleProps} className="stroke-border" />
      <circle
        {...circleProps}
        className={strokeClassName}
        strokeLinecap="round"
        strokeDasharray={`${filledLength} ${CIRCUMFERENCE}`}
      />
    </svg>
  );
}
