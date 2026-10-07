// Display formatting for the ISO dates ("2026-10-07") the server sends. The server decides which
// day things happened on; these only choose how a given day is written.
function parseDay(isoDate: string): Date {
  return new Date(`${isoDate}T00:00:00`);
}

export const weekdayInitial = (isoDate: string) =>
  parseDay(isoDate).toLocaleDateString("en", { weekday: "narrow" });

export const formatMonthYear = (isoDate: string) =>
  parseDay(isoDate).toLocaleDateString("en", { month: "long", year: "numeric" });

export const formatMonthDay = (isoDate: string) =>
  parseDay(isoDate).toLocaleDateString("en", { month: "short", day: "numeric" });
