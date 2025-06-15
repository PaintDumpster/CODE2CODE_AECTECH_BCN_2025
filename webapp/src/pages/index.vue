<template>
  <div style="height: 100vh; display: flex; flex-direction: column;">
    <!-- Top Bar: IFC Upload and View Switcher -->
    <div class="d-flex align-center mb-4 pa-4" style="gap: 16px; background-color: #f5f5f5;">
      <!-- IFC Upload Button -->
      <label class="v-btn v-btn--outlined v-btn--density-default" style="cursor:pointer;">
        <input type="file" accept=".ifc" style="display:none" @change="onFileChange" />
        Upload IFC File
      </label>
      <!-- View Switcher -->
      <v-btn-toggle v-model="viewMode" mandatory>
        <v-btn value="graph">Graph View</v-btn>
        <v-btn value="overlap">Split View</v-btn>
        <v-btn value="model">3D Model View</v-btn>
      </v-btn-toggle>
    </div>

    <!-- Main Content Area -->
    <div class="d-flex" style="flex: 1; overflow: hidden;">
      <!-- Chat Window -->
      <div style="width: 25%; border-right: 1px solid #ddd;">
        <ChatWindow_Completed />
      </div>

      <!-- Split View Container -->
      <div style="width: 75%; display: flex;">
        <!-- Left side: Graph View -->
        <div :style="{
          width: viewMode === 'model' ? '0%' : viewMode === 'overlap' ? '50%' : '100%',
          transition: 'width 0.3s ease',
          borderRight: viewMode === 'overlap' ? '1px solid #ddd' : 'none'
        }">
          <GraphViewer />
        </div>
        <!-- Right side: IFC Viewer -->
        <div :style="{
          width: viewMode === 'graph' ? '0%' : viewMode === 'overlap' ? '50%' : '100%',
          transition: 'width 0.3s ease'
        }">
          <IFCViewer :ifcFile="ifcFile" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import GraphViewer from '@/components/GraphViewer.vue'
import IFCViewer from '@/components/IFCViewer.vue'
import ChatWindow_Completed from '@/components/ChatWindow_Completed.vue'

const viewMode = ref('overlap')
const ifcFile = ref(null)

function onFileChange(event) {
  const file = event.target.files[0]
  ifcFile.value = file || null
}
</script>

<style scoped>
.d-flex {
  display: flex;
}
</style>
