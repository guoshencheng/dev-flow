import { cancel } from './modules/reservations/application/cancel.mjs';
import { resetReservations } from './modules/reservations/infrastructure/store.mjs';
import { refundRows } from './modules/billing/infrastructure/store.mjs';

resetReservations([{ id: 'r-1', ownerId: 'u-1', status: 'active', price: 120,
  startAt: 100 * 3600_000 }]);
console.log(JSON.stringify({ reservation: cancel({ reservationId: 'r-1', actorId: 'u-1', now: 0 }),
  refunds: refundRows() }));
