import test from 'node:test';
import assert from 'node:assert/strict';
import { cancel } from '../src/modules/reservations/application/cancel.mjs';
import { resetReservations } from '../src/modules/reservations/infrastructure/store.mjs';
import { refundRows, resetRefunds } from '../src/modules/billing/infrastructure/store.mjs';

function setup() {
  resetReservations([{ id: 'r-1', ownerId: 'u-1', status: 'active', price: 120,
    startAt: 100 * 3600_000 }]);
  resetRefunds();
}
test('本人提前取消并登记退款', () => {
  setup();
  assert.equal(cancel({ reservationId: 'r-1', actorId: 'u-1', now: 0 }).status, 'cancelled');
  assert.deepEqual(refundRows(), [{ reservationId: 'r-1', amount: 120 }]);
});
test('拒绝其他用户取消', () => {
  setup();
  assert.throws(() => cancel({ reservationId: 'r-1', actorId: 'u-2', now: 0 }), /FORBIDDEN/);
  assert.deepEqual(refundRows(), []);
});
