export function convertToGraphFormat(nodeData, edgeData){
  let nodes = []
  let nodeProperties = Object.keys(nodeData)
  Object.keys(nodeData.GlobalId).forEach(id => {
    let node = {id: id}
    nodeProperties.forEach(prop => {
      if (prop != 'GlobalId'){
        node[prop] = nodeData[prop][id]
      }
    })
    let nodeLabel = '';
    nodeProperties.forEach((prop) => {
        if (prop !== 'GlobalId' && nodeData[prop]?.[id] != null) {
        nodeLabel += `${prop}: ${nodeData[prop][id]}\n`;
        }
    });
    node.nodeLabel = nodeLabel.trim();
    nodes.push(node)
  })
  
  const links = Object.keys(edgeData.source).map((index) => {
    const link = {
      source: edgeData.source[index],
      target: edgeData.target[index],
    };
    const edgeAttributes = edgeData.attributes[index];
    if (edgeAttributes && typeof edgeAttributes === 'object') {
      Object.keys(edgeAttributes).forEach((attr) => {
        link[attr] = edgeAttributes[attr];
      });
    }
    return link;
  });

  let formattedData = {
    nodes: nodes,
    links: links
  }
  return formattedData
}