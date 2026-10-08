import assert from 'node:assert/strict';
import { cancel } from '../../../src/modules/reservations/application/cancel.mjs';
import { cancelReservation } from '../../../src/modules/reservations/domain.mjs';
import { resetReservations, getReservation } from '../../../src/modules/reservations/infrastructure/store.mjs';
import { resetRefunds, refundRows } from '../../../src/modules/billing/infrastructure/store.mjs';
import { refund } from '../../../src/modules/billing/application/refund.mjs';
const H=3600_000;
function setup(startAt=100*H) {resetReservations([{id:'r-1',ownerId:'u-1',status:'active',price:120,startAt}]);resetRefunds();}
let failed=0;
function check(name, fn) {try {fn(); console.log('PASS '+name);} catch(e) {failed++; console.log('FAIL '+name+' '+e.message);}}
check('RULE-03 重复取消仅一笔退款',()=>{setup();cancel({reservationId:'r-1',actorId:'u-1',now:0});cancel({reservationId:'r-1',actorId:'u-1',now:0});assert.equal(refundRows().length,1);});
check('RULE-02 恰好24小时全额退款',()=>{setup(24*H);let r=cancel({reservationId:'r-1',actorId:'u-1',now:0});assert.equal(r.refundAmount,120);assert.equal(refundRows().length,1);});
check('RULE-02 不足24小时取消不退款',()=>{setup(24*H-1);let r=cancel({reservationId:'r-1',actorId:'u-1',now:0});assert.equal(r.status,'cancelled');assert.equal(r.refundAmount,0);assert.deepEqual(refundRows(),[]);});
check('RULE-01 非本人拒绝且预约退款均不变',()=>{setup();let before=structuredClone(getReservation('r-1'));assert.throws(()=>cancel({reservationId:'r-1',actorId:'u-2',now:0}),/FORBIDDEN/);assert.deepEqual(getReservation('r-1'),before);assert.deepEqual(refundRows(),[]);});
check('不存在预约被拒绝且数据不变',()=>{setup();let before=structuredClone(getReservation('r-1'));assert.throws(()=>cancel({reservationId:'missing',actorId:'u-1',now:0}),/NOT_FOUND/);assert.deepEqual(getReservation('r-1'),before);assert.deepEqual(refundRows(),[]);});
check('ARC-01 领域计算不写存储',()=>{setup();let before=structuredClone(getReservation('r-1'));cancelReservation({...before},0);assert.deepEqual(getReservation('r-1'),before);});
check('ARC-02 已有结算公开用例自身去重',()=>{setup();refund({reservationId:'r-1',amount:120});refund({reservationId:'r-1',amount:120});assert.equal(refundRows().length,1);});
console.log(JSON.stringify({checks:7,passed:7-failed,failed}));process.exitCode=failed?1:0;
