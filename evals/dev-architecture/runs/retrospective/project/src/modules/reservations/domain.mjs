import { saveReservation } from './infrastructure/store.mjs';

export function cancelReservation(reservation, now) {
  if (reservation.status === 'cancelled') return { ...reservation };
  const refundAmount = reservation.startAt - now >= 24 * 3600_000 ? reservation.price : 0;
  const cancelled = { ...reservation, status: 'cancelled', refundAmount };
  saveReservation(cancelled);
  return cancelled;
}
