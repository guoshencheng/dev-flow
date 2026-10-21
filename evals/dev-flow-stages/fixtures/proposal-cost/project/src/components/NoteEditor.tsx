import { useState } from "react";
export function NoteEditor({ initial, onSave }: { initial: string; onSave: (text: string) => Promise<void> }) {
  const [text, setText] = useState(initial);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  async function save() {
    setSaving(true); setError("");
    try { await onSave(text); } catch (e) { setError((e as Error).message); } finally { setSaving(false); }
  }
  return <section><textarea value={text} onChange={e => setText(e.target.value)} />
    <button disabled={saving} onClick={save}>{saving ? "保存中" : "保存"}</button>{error && <p role="alert">{error}</p>}</section>;
}
