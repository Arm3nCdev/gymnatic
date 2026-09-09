import { defineConfig } from 'orval';

export default defineConfig({
  gymbro: {
    input: './openapi.json',
    output: {
      mode: 'tags-split',
      target: 'src/api/endpoints',
      schemas: 'src/api/model',
      client: 'react-query',
    },
  },
});
