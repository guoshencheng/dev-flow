const refunds = [];
export function writeRefund(reservationId, amount) { refunds.push({ reservationId, amount }); }
export function refundRows() { return refunds.map(value => ({ ...value })); }
export function resetRefunds() { refunds.length = 0; }
