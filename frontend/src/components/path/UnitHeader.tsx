import { Icon } from "@/components/ui/Icon";
import { getUnitColorClasses } from "@/lib/unitColors";
import type { PathUnit } from "@/lib/types";

export function UnitHeader({ unit }: { unit: PathUnit }) {
  const colors = getUnitColorClasses(unit.color);

  // top-14 clears MobileTopBar (h-14) below lg. z-10 is the lowest layer: mobile bars (z-30),
  // the popover click-away layer (z-40) and the popover (z-50) all sit above the banner.
  return (
    <div
      className={`sticky top-14 z-10 flex items-center justify-between rounded-2xl border-b-4 p-4 text-surface lg:top-4 ${colors.fill} ${colors.shade}`}
    >
      <div>
        <p className="text-sm font-extrabold uppercase tracking-[0.8px] text-surface/80">
          {unit.title}
        </p>
        <h2 className="text-xl font-extrabold">{unit.description}</h2>
      </div>
      <button
        disabled
        title="Coming soon"
        aria-label="Guidebook (coming soon)"
        className="flex items-center gap-2 rounded-xl border-2 border-surface/30 bg-surface/10 px-3 py-2 text-sm font-extrabold uppercase tracking-[0.8px]"
      >
        <Icon name="notebook" className="h-6 w-6" />
        <span className="hidden sm:inline">Guidebook</span>
      </button>
    </div>
  );
}
