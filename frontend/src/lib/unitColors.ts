// Tailwind only generates classes it can see as whole strings, so each unit colour
// token maps to literal class names instead of being interpolated.
export interface UnitColorClasses {
  fill: string;
  shade: string;
  nodeShadow: string;
  stroke: string;
  text: string;
}

const UNIT_COLOR_CLASSES: Record<string, UnitColorClasses> = {
  green: {
    fill: "bg-green",
    shade: "border-green-shade",
    nodeShadow: "shadow-node-green",
    stroke: "stroke-green",
    text: "text-green",
  },
  blue: {
    fill: "bg-blue",
    shade: "border-blue-shade",
    nodeShadow: "shadow-node-blue",
    stroke: "stroke-blue",
    text: "text-blue",
  },
  purple: {
    fill: "bg-purple",
    shade: "border-purple-shade",
    nodeShadow: "shadow-node-purple",
    stroke: "stroke-purple",
    text: "text-purple",
  },
};

export function getUnitColorClasses(color: string): UnitColorClasses {
  return UNIT_COLOR_CLASSES[color] ?? UNIT_COLOR_CLASSES.green;
}
