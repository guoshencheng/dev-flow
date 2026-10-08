import { cancel } from './modules/reservations/application/cancel.mjs';
import { resetReservations, getReservation } from './modules/reservations/infrastructure/store.mjs';
import { refundRows } from './modules/billing/infrastructure/store.mjs';

resetReservations([{ id: 'r-1', ownerId: 'u-1', status: 'active', price: 120,
  startAt: 100 * 3600_000 }]);
console.log(JSON.stringify({ reservation: cancel({ reservationId: 'r-1', actorId: 'u-1', now: 0 }),
  refunds: refundRows() }));

const { reservationSummary } = await import('./modules/reservations/public.mjs');
const { exportSummaries } = await import('./modules/reporting/application/export.mjs');
console.log(JSON.stringify({ summaries: exportSummaries(['r-1', 'missing'],
  id => reservationSummary(id, getReservation)) }));
