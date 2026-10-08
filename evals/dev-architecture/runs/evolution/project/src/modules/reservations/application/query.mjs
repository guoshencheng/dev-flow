export function reservationSummary(id, readReservation) {
  const value = readReservation(id);
  if (!value) return null;
  return { id: value.id, status: value.status, price: value.price };
}
