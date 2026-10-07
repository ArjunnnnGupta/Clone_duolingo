// Horizontal offset (px) per node position; repeating it makes the path snake left and right.
const ZIG_ZAG_OFFSETS_PX = [0, 45, 70, 45, 0, -45, -70, -45];

export function getNodeOffset(nodeIndex: number): number {
  return ZIG_ZAG_OFFSETS_PX[nodeIndex % ZIG_ZAG_OFFSETS_PX.length];
}
