<template>
  <div id="3d-graph"></div> 
</template>

<script setup>
import ForceGraph3D from '3d-force-graph';
import { onMounted, watch } from 'vue'
import {convertToGraphFormat} from "@/utils/index"
import {useStore} from '@/stores/store'
import { storeToRefs } from 'pinia'

const store = useStore()
const { highlightedNodes } = storeToRefs(store)
let Graph = null

onMounted(async () => {
  //Step 1: Get the nodes and edges
  const [nodesRes, edgesRes] = await Promise.all([
      fetch('/nodes.json'),
      fetch('/edges.json')
    ]);

  const nodeData = await nodesRes.json();
  const edgeData = await edgesRes.json();

  //Step 2: Format the data into the structure expected by ForceGraph3D and store it globally
  let formattedGraphJson = convertToGraphFormat(nodeData, edgeData)
  store.graphJSON = formattedGraphJson

  //Step 3: Get the HTML element where we want to render the graph
  let graphDiv = document.getElementById('3d-graph')

  //Step 4: Create the ForceGraph3D (https://github.com/vasturiano/3d-force-graph)
  Graph = new ForceGraph3D(graphDiv)
    .graphData(formattedGraphJson)
    .nodeLabel('nodeLabel')
    .nodeAutoColorBy('IfcType')
    .nodeColor(node => highlightedNodes.value.has(node.id) ? 'red' : null)
})

// Watch for changes in highlightedNodes and update the graph
watch(highlightedNodes, () => {
  if (Graph) {
    Graph.nodeColor(node => highlightedNodes.value.has(node.id) ? 'red' : null)
  }
})
</script>

<style scoped>

</style>
