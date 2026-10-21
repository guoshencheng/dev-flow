import { Order } from "../api/orders";
export function OrderList({ orders, openDetail }: { orders: Order[]; openDetail: (id: string) => void }) {
  return <table><tbody>{orders.map(order => <tr key={order.id}><td>{order.note}</td>
    <td><button onClick={() => openDetail(order.id)}>查看详情</button></td></tr>)}</tbody></table>;
}
