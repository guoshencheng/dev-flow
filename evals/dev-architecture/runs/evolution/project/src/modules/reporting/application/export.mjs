export function exportSummaries(ids, readSummary) {
  return ids.map(id => readSummary(id)).filter(value => value !== null);
}
