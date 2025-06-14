const { regulationTextToSchema } = require('../nltojson');

(async () => {
  const rule = "Fire doors in escape routes must have a fire rating of at least EI 60.";
  
  try {
    const jsonSchema = await regulationTextToSchema(rule);
    console.log("✅ Generated JSON schema:\n", JSON.stringify(jsonSchema, null, 2));
  } catch (err) {
    console.error("❌ Test failed:", err.message);
  }
})();
