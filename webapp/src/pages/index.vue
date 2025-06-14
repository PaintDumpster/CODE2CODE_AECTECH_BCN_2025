<template>
  <div>
    <!-- Top Bar: IFC Upload and View Switcher -->
    <div class="d-flex align-center mb-4" style="gap: 16px;">
      <!-- IFC Upload Button -->
      <label class="v-btn v-btn--outlined v-btn--density-default" style="cursor:pointer;">
        <input type="file" accept=".ifc" style="display:none" />
        Upload IFC File
      </label>
      <!-- View Switcher -->
      <v-btn-toggle v-model="viewMode" mandatory>
        <v-btn value="graph">Graph View</v-btn>
        <v-btn value="model">3D Model View</v-btn>
        <v-btn value="overlap">Overlap View</v-btn>
      </v-btn-toggle>
    </div>
    <div class="d-flex">
      <div style="width: 25%;">
        <ChatWindow_Completed />
      </div>
      <div style="width: 75%;">
        <GraphViewer />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const viewMode = ref('graph')
</script>
