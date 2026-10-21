import { Order, updateNote } from "../api/orders";
import { NoteEditor } from "../components/NoteEditor";
export function OrderDetail({ order, onUpdated }: { order: Order; onUpdated: (next: Order) => void }) {
  return <main><h1>订单 {order.id}</h1>{order.canEdit ?
    <NoteEditor initial={order.note} onSave={async text => onUpdated(await updateNote(order.id, text))} /> : <p>{order.note}</p>}</main>;
}
