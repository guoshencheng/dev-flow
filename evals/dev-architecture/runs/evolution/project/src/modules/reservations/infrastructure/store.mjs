const rows = new Map();
export function resetReservations(values) {
  rows.clear();
  for (const value of values) rows.set(value.id, { ...value });
}
export function getReservation(id) { return rows.get(id); }
export function saveReservation(value) { rows.set(value.id, { ...value }); }
