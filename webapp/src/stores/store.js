// Utilities
import { defineStore } from 'pinia'

export const useStore = defineStore('app', {
  state: () => ({
    graphJSON: null,
    highlightedNodes: new Set()
  }),
  actions: {
    highlightNodes(nodeIds) {
      this.highlightedNodes = new Set(nodeIds)
    }
  }
})
