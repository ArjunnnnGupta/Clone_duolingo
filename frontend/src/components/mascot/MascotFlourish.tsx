import { Mascot } from "./Mascot";

interface MascotFlourishProps {
  side: "left" | "right";
}

export function MascotFlourish({ side }: MascotFlourishProps) {
  const sideStyle =
    side === "left" ? { right: "calc(50% + 100px)" } : { left: "calc(50% + 100px)" };

  return (
    <div
      className="pointer-events-none absolute top-1/2 -translate-y-1/2"
      style={sideStyle}
    >
      <Mascot className="h-16 w-16" />
    </div>
  );
}
