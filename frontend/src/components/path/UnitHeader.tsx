import { getUnitColorClasses } from "@/lib/unitColors";
import { GuidebookButton } from "./GuidebookButton";
import type { PathUnit } from "@/lib/types";

export function UnitHeader({ unit }: { unit: PathUnit }) {
  const colors = getUnitColorClasses(unit.color);

  // top-14 clears MobileTopBar (h-14) below lg. z-10 is the lowest layer: mobile bars (z-30),
  // the popover click-away layer (z-40) and the popover (z-50) all sit above the banner.
  return (
    <div
      className={`sticky top-14 z-10 flex items-center justify-between rounded-2xl border-b-4 p-4 text-on-color lg:top-4 ${colors.fill} ${colors.shade}`}
    >
      <div>
        <p className="text-sm font-extrabold uppercase tracking-[0.8px] text-on-color/80">
          {unit.title}
        </p>
        <h2 className="text-xl font-extrabold">{unit.description}</h2>
      </div>
      <GuidebookButton />
    </div>
  );
}
