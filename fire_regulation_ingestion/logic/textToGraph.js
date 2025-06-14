const path = require('path');
console.log('✅ __dirname:', __dirname);
console.log('✅ Resolved neo4j path:', path.resolve(__dirname, '../db/neo4j.js'));


const neo4jPath = path.resolve(__dirname, '../db/neo4j.js');
const { getDriver, runCypher } = require(neo4jPath);


require('dotenv').config();
const { regulationTextToSchema } = require('./nltojson.js');
const { transformToCypher } = require('./transformToCypher');
const neo4jModulePath = path.resolve(__dirname, '../db/neo4j.js');
;

async function main() {
  // 🔤 Step 1: Enter your regulation here
  const input = "Fire doors in escape routes must have a fire rating of at least EI 60.";

  console.log(`📥 Input: "${input}"`);

  // 🔁 Step 2: Natural language → Normalized JSON
  const schema = await regulationTextToSchema(input);
  console.log("📦 Generated schema:\n", JSON.stringify(schema, null, 2));

  // 💡 Step 3: JSON → Cypher
  const cyphers = transformToCypher(schema);
  console.log("\n🧠 Generated Cypher:\n", cyphers.join('\n---\n'));

  // 🚀 Step 4: Push to Neo4j
  const driver = getDriver();
  const session = driver.session();

  try {
    for (const cypher of cyphers) {
      await runCypher(session, cypher);
      console.log(`✅ Executed: ${cypher.trim().slice(0, 80)}...`);
    }
    console.log("\n🎉 Regulation successfully ingested into the graph.");
  } catch (err) {
    console.error("❌ Import failed:", err.message);
  } finally {
    await session.close();
    await driver.close();
  }
}

main();
