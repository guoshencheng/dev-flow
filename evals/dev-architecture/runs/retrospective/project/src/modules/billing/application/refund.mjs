import { writeRefund, refundRows } from '../infrastructure/store.mjs';

export function refund({ reservationId, amount }) {
  if (amount <= 0) throw new Error('INVALID_AMOUNT');
  const previous = refundRows().find(row => row.reservationId === reservationId);
  if (previous) return previous;
  writeRefund(reservationId, amount);
  return { reservationId, amount };
}
