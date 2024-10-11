const atlasapprox = require('./index.js');

test('api version', async () => {
  const result = atlasapprox.api_version;
  expect(result.startsWith('v')).toBe(true);
});

test('measurement types', async () => {
  const result = await atlasapprox.measurement_types();
  expect(result).toBeDefined();
  expect(result).toHaveProperty("measurement_types");
  expect(result["measurement_types"]).toContain("gene_expression");
});

test('organisms', async () => {
  const result = await atlasapprox.organisms({});
  expect(result).toBeDefined();
  expect(result).toHaveProperty("measurement_type");
  expect(result).toHaveProperty("organisms");
  expect(result["organisms"]).toContain("h_sapiens");
});
