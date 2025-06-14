<template>
  <div style="height: 100vh;" class="d-flex flex-column">
    <!-- Logo -->
    <div class="d-flex justify-left align-center">
      <img src="@/assets/logo.png" alt="Logo" 
        style="height: 50px;" />
    </div>
    
    <!-- Mode Toggle -->
    <div class="d-flex justify-center align-center mb-2">
      <v-btn-toggle v-model="mode" mandatory>
        <v-btn value="openai">OpenAI</v-btn>
        <v-btn value="backend">Backend NL→Cypher</v-btn>
      </v-btn-toggle>
    </div>

    <!-- CHAT MESSAGES -->
    <div style="overflow-y: auto; flex-grow: 1;" class="pa-2">
      <div v-for="message in allMessages" 
        class="d-flex" :class="message.type === 'userMessage' ? 'justify-end' : 'justify-start'">
        <!-- User Message -->
        <span v-if="message.type == 'userMessage'" 
          class="pa-2 my-2 rounded-lg"
          style="background-color: lightgray;">
          {{ message.message }}
        </span>
        <!-- AI Response -->
        <span v-else v-html="message.message" class="ml-6"></span>
    </div>
    </div>

    <!-- Textarea and send button -->
    <div class="pa-2" style="border-top: 1px solid #ddd;">
      <v-textarea 
        v-model="inputMessage"
        hide-details
        variant="outlined"
        auto-grow
        label="Ask your graph questions here"
      />
      <div class="d-flex justify-end mt-2">
        <v-btn
          @click="sendRequest"
          :loading="sendLoading"
          size="small"
          icon
          variant="text"
          class="bg-black"
        >
          <v-icon>mdi-arrow-up</v-icon>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { OpenAI } from 'openai'
import {useStore} from '@/stores/store'

const store = useStore()

//Initialize Variables
const inputMessage = ref('')
const allMessages = ref([])
var sendLoading = ref(false)
const mode = ref('openai') // 'openai' or 'backend'

//Create OpenAI Connection
const openai = new OpenAI({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY,
  dangerouslyAllowBrowser: true
})

async function sendRequest(){
  sendLoading.value = true
  
  allMessages.value.push({
    message: inputMessage.value,
    type: 'userMessage'
  })

  if (mode.value === 'openai') {
    const graphjson = store.graphJSON
    
    let compressed = compressGraphData(graphjson)

    try {
      const response = await openai.chat.completions.create({
        model: 'gpt-4o',
        messages: [
          { role: 'system', content: 'You are a graph analyst. Answer questions about a network graph structure that is generated from building IFC data. When you respond please give your answer in html format, but please dont wrap the response in any extra text like ```html.' },
          {
            role: 'user',
            content: `This is the graph structure (nodes and links in JSON format):\n\n${JSON.stringify(compressed)}\n\nPlease answer the following question:\n${inputMessage.value}`
          }
        ]
      })

      console.log(response)

      const aiMessage = response?.choices?.[0]?.message?.content

      if (!aiMessage) {
        console.warn('No AI message found in response.')
      } else {
        allMessages.value.push({
          message: aiMessage,
          type: 'openAIResponse'
        })
      }
    } catch (error) {
      allMessages.value.push({
        message: 'Error: Unable to process your request at the moment.',
        type: 'openAIResponse'
      })
    }
  } else if (mode.value === 'backend') {
    // Backend NL-to-Cypher mode
    try {
      const response = await fetch('http://localhost:3001/api/nl-query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: inputMessage.value })
      })
      const data = await response.json()
      if (data.error) {
        allMessages.value.push({
          message: `Backend error: ${data.error}`,
          type: 'backendError'
        })
      } else {
        allMessages.value.push({
          message: `<b>Cypher:</b> <pre>${data.cypher}</pre><br/><b>Explanation:</b> ${data.explanation}<br/><b>Raw Data:</b> <pre>${JSON.stringify(data.rawData, null, 2)}</pre>`,
          type: 'backendResponse'
        })
        // Try to highlight the first node in the rawData if present
        if (Array.isArray(data.rawData) && data.rawData.length > 0) {
          const first = data.rawData[0]
          // Try to find a property that looks like an ID
          let nodeId = null
          if (first.id) nodeId = first.id
          else if (first.n && first.n.id) nodeId = first.n.id
          else if (first.n && first.n.GlobalId) nodeId = first.n.GlobalId
          if (nodeId) store.highlightedNodeId = nodeId
        }
      }
    } catch (error) {
      allMessages.value.push({
        message: `Backend error: ${error.message}`,
        type: 'backendError'
      })
    }
  }
  inputMessage.value = ''
  sendLoading.value = false
}

function compressGraphData(original) {
  const nodeIdMap = new Map();
  const compressedNodes = [];
  const compressedLinks = [];

  original.nodes.forEach((node, index) => {
    const shortId = `n${index}`;
    nodeIdMap.set(node.id, shortId);

    compressedNodes.push({
      id: shortId,
      name: node.Name,
      type: node.IfcType,
      category: node.category,
      description: node.Description
    });
  });

  original.links.forEach((link, index) => {
    const sourceId = nodeIdMap.get(link.source.id || link.source);
    const targetId = nodeIdMap.get(link.target.id || link.target);

    compressedLinks.push({
      source: sourceId,
      target: targetId,
    });
  });

  return {
    nodes: compressedNodes,
    links: compressedLinks
  };
}

async function sendCypherQuery(cypher) {
  try {
    const response = await fetch('http://localhost:3000/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cypher })
    });
    const data = await response.json();
    return data;
  } catch (error) {
    return { error: error.message };
  }
}
</script>

<style scoped>
</style>