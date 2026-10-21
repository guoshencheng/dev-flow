export type Order = { id: string; note: string; canEdit: boolean };
export async function readOrder(id: string): Promise<Order> {
  const response = await fetch(`/api/orders/${id}`);
  if (!response.ok) throw new Error("读取失败");
  return response.json();
}
export async function updateNote(id: string, note: string): Promise<Order> {
  const response = await fetch(`/api/orders/${id}/note`, {
    method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ note })
  });
  if (!response.ok) throw new Error(response.status === 403 ? "无编辑权限" : "保存失败，请重试");
  return response.json();
}
