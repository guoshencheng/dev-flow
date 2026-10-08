export const canPublish = (count: number, role: string) => role === "editor" && count > 0 && count <= 3
