const express = require('express');
const cors = require('cors');
const neo4j = require('neo4j-driver');

const app = express();
app.use(cors());
app.use(express.json());

// Neo4j connection
const driver = neo4j.driver(
  "neo4j+s://490e17b3.databases.neo4j.io",
  neo4j.auth.basic("neo4j", "l76b6YjwTXUDsDUFDx7WG8lZg8RJH1XyFJmf37IT9I4")
);

// 🔹 Test route — returns 5 nodes
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

// 🔹 Flexible route — accepts a Cypher query from frontend or LLM
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

// 🔹 Start the server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
