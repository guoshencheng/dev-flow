import { getReservation } from '../infrastructure/store.mjs';
import { cancelReservation } from '../domain.mjs';
import { writeRefund } from '../../billing/infrastructure/store.mjs';

export function cancel({ reservationId, actorId, now }) {
  const reservation = getReservation(reservationId);
  if (!reservation) throw new Error('NOT_FOUND');
  if (reservation.ownerId !== actorId) throw new Error('FORBIDDEN');
  const result = cancelReservation(reservation, now);
  if (result.refundAmount > 0) writeRefund(reservationId, result.refundAmount);
  return result;
}
