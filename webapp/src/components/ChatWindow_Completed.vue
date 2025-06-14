<template>
  <div style="height: 100vh;" class="d-flex flex-column">
    <!-- Logo -->
    <div class="d-flex justify-left align-center">
      <img src="@/assets/logo.png" alt="Logo" 
        style="height: 50px;" />
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

//Create OpenAI Connection
const openai = new OpenAI({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY,
  dangerouslyAllowBrowser: true
})

async function sendRequest(){
  sendLoading = true
  
  allMessages.value.push({
    message: inputMessage.value,
    type: 'userMessage'
  })

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
  inputMessage.value = ''
  sendLoading = false
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
</script>

<style scoped>
</style>