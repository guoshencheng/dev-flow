import assert from 'node:assert/strict';
import { reservationSummary } from '../../../src/modules/reservations/public.mjs';
import { exportSummaries } from '../../../src/modules/reporting/application/export.mjs';
import { cancel } from '../../../src/modules/reservations/application/cancel.mjs';
import { getReservation, resetReservations } from '../../../src/modules/reservations/infrastructure/store.mjs';
import { refundRows, resetRefunds } from '../../../src/modules/billing/infrastructure/store.mjs';
let passed=0,failed=0;
function check(name,fn){try{fn();passed++;console.log('PASS '+name);}catch(e){failed++;console.log('FAIL '+name+' '+e.message);}}
const input={id:'r-1',ownerId:'u-1',status:'active',price:120,startAt:100*3600_000};
check('公开摘要查询仅输出id/status/price且不修改注入对象',()=>{let row=structuredClone(input);let before=structuredClone(row);assert.deepEqual(reservationSummary('r-1',()=>row),{id:'r-1',status:'active',price:120});assert.deepEqual(row,before);});
check('不存在预约返回null',()=>assert.equal(reservationSummary('missing',()=>undefined),null));
check('报表消费者注入查询契约并跳过null保留顺序',()=>{const ids=['r-1','missing','r-2'];let calls=[];let result=exportSummaries(ids,id=>{calls.push(id);return id==='missing'?null:{id,status:'active',price:120};});assert.deepEqual(calls,ids);assert.deepEqual(result.map(x=>x.id),['r-1','r-2']);assert.deepEqual(ids,['r-1','missing','r-2']);});
check('空id列表导出空摘要且不访问查询',()=>assert.deepEqual(exportSummaries([],()=>{throw Error('unexpected read');}),[]));
check('取消之后真实内存适配导出可序列化摘要且预约/退款不变',()=>{resetReservations([input]);resetRefunds();cancel({reservationId:'r-1',actorId:'u-1',now:0});const before={reservation:structuredClone(getReservation('r-1')),refunds:refundRows()};const result=exportSummaries(['r-1','missing'],id=>reservationSummary(id,getReservation));assert.deepEqual(JSON.parse(JSON.stringify(result)),[{id:'r-1',status:'cancelled',price:120}]);result[0].status='changed';assert.deepEqual({reservation:getReservation('r-1'),refunds:refundRows()},before);});
console.log(JSON.stringify({checks:passed+failed,passed,failed}));process.exitCode=failed?1:0;
