async function runCypher(cypher, driver) {
    const session = driver.session();
  
    try {
      const result = await session.run(cypher);
      const records = result.records.map(record => record.toObject());
      return records;
    } catch (err) {
      console.error('Cypher query failed:', err);
      throw err;
    } finally {
      await session.close();
    }
  }
  
  module.exports = {
    runCypher
  };