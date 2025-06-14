require('dotenv').config();
const { OpenAI } = require('openai');
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function regulationTextToSchema(naturalText) {
  const prompt = `
You are a structured data converter for building fire safety regulations.

Convert the following natural language rule into a valid JSON object with this structure:

{
  "type": "IfcType",
  "conditions": [
    {
      "property": "PropertyName",
      "relationship": "RELATIONSHIP_TYPE",
      "value": "SomeValue"
    }
  ]
}

Only use these exact relationship types: EQUALS, HIGHER_THAN, LOWER_THAN, SMALLER_THAN.
Only use standardized building elements like IfcDoor, IfcWall, IfcSlab, IfcWindow, IfcStair, etc.
Do not wrap your response in markdown or code blocks.

Text: "${naturalText}"
`;

  const response = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0,
  });

  const rawText = response.choices[0].message.content.trim();

  let schema;
  try {
    schema = JSON.parse(rawText);
  } catch (err) {
    console.error("❌ Failed to parse JSON:", rawText);
    throw new Error("LLM response was not valid JSON.");
  }

  // 🔧 Normalize the JSON structure
  return normalizeSchema(schema);
}

function normalizeSchema(schema) {
  const typeMap = {
    FireDoor: 'IfcDoor',
    Wall: 'IfcWall',
    Slab: 'IfcSlab',
    Roof: 'IfcRoof',
    Window: 'IfcWindow',
    Stair: 'IfcStair',
    Ramp: 'IfcRamp',
    Column: 'IfcColumn',
    Beam: 'IfcBeam',
    Door: 'IfcDoor',
  };

  const relationshipMap = {
    atLeast: 'HIGHER_THAN',
    greaterThan: 'HIGHER_THAN',
    moreThan: 'HIGHER_THAN',
    lessThan: 'LOWER_THAN',
    atMost: 'LOWER_THAN',
    smallerThan: 'SMALLER_THAN',
    equals: 'EQUALS',
    equalTo: 'EQUALS',
  };

  const normalized = {
    type: typeMap[schema.type] || schema.type,
    conditions: (schema.conditions || []).map(cond => ({
      property: capitalize(cond.property),
      relationship: relationshipMap[cond.relationship] || cond.relationship,
      value: cond.value
    }))
  };

  return normalized;
}

function capitalize(str) {
  if (!str || typeof str !== 'string') return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
}

module.exports = { regulationTextToSchema };
