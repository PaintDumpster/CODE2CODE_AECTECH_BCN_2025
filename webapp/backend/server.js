const express = require('express');
const cors = require('cors');
const neo4j = require('neo4j-driver');
const openaiModule = require('./openai');
console.log(openaiModule);
const { naturalLanguageToCypher, summarizeQueryResult } = openaiModule;
const { runCypher } = require('./graph');

const app = express();
app.use(cors());
app.use(express.json());

// Neo4j connection
const driver = neo4j.driver(
  "neo4j+s://490e17b3.databases.neo4j.io",
  neo4j.auth.basic("neo4j", "l76b6YjwTXUDsDUFDx7WG8lZg8RJH1XyFJmf37IT9I4")
);

// Test route (optional)
app.get('/api/nodes', async (req, res) => {
  const session = driver.session();

  try {
    const result = await session.run('MATCH (n) RETURN n LIMIT 5');
    const nodes = result.records.map(record => record.get('n').properties);
    res.json(nodes);
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    await session.close();
  }
});

// Raw Cypher query route
app.post('/api/query', async (req, res) => {
  const { cypher } = req.body;
  const session = driver.session();

  try {
    const result = await session.run(cypher);
    const records = result.records.map(record => record.toObject());
    res.json(records);
  } catch (err) {
    res.status(400).json({ error: err.message });
  } finally {
    await session.close();
  }
});

// Natural language query route
app.post('/api/nl-query', async (req, res) => {
  const { question } = req.body;

  try {
    // Step 1: NL → Cypher
    const cypher = await naturalLanguageToCypher(question);

    // Step 2: Run Cypher on Neo4j
    const result = await runCypher(cypher, driver);

    // Step 3: LLM explains the result
    const explanation = await summarizeQueryResult(result);

    res.json({
      cypher,
      explanation,
      rawData: result
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});