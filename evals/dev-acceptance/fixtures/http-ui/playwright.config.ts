import { defineConfig } from '@playwright/test';

const port = Number(process.env.EVAL_PORT);
if (!Number.isInteger(port) || port < 1) throw new Error('显式提供 EVAL_PORT');
const baseURL = `http://127.0.0.1:${port}`;
export default defineConfig({
  testDir: './tests',
  workers: 1,
  retries: 0,
  timeout: 15000,
  expect: { timeout: 4000 },
  reporter: [['json', { outputFile: process.env.EVAL_RESULT_FILE || 'result.json' }]],
  use: {
    baseURL,
    browserName: 'chromium',
    launchOptions: { executablePath: process.env.EVAL_BROWSER_EXECUTABLE },
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'node server.mjs',
    url: `${baseURL}/health`,
    reuseExistingServer: false,
    gracefulShutdown: { signal: 'SIGTERM', timeout: 2000 },
    timeout: 10000,
  },
});
