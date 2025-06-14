const { OpenAI } = require('openai');
require('dotenv').config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function naturalLanguageToCypher(question) {
  const prompt = `
You are a Cypher expert. Translate the following natural language question into a Cypher query that works on a Neo4j graph.
The graph contains nodes like IfcWall, IfcSlab, and FireSector, and relationships like PART_OF and CONNECTS_TO.
Question: "${question}"
Cypher:
`;

  const response = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0
  });

  const cypher = response.choices[0].message.content.trim();
  return cypher;
}

async function summarizeQueryResult(jsonData) {
  const prompt = `
Here is the result of a Cypher query returned from a Neo4j graph in JSON format.
Summarize what this result means in one sentence for a general user.
Data:
\`\`\`json
${JSON.stringify(jsonData, null, 2)}
\`\`\`
`;

  const response = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.7
  });

  const explanation = response.choices[0].message.content.trim();
  return explanation;
}

module.exports = {
  naturalLanguageToCypher,
  summarizeQueryResult
};