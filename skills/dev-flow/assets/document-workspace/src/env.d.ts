/// <reference types="vite/client" />
declare module 'virtual:design-mdx' {
  const loaders: Record<string, () => Promise<{ default: import('react').ComponentType<{ components?: Record<string, unknown> }> }>>;
  export default loaders;
}
declare module 'mammoth/mammoth.browser' {
  const mammoth: { convertToHtml(input: { arrayBuffer: ArrayBuffer }): Promise<{ value: string; messages: { message: string }[] }> };
  export default mammoth;
}
