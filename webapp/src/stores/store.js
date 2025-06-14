// Utilities
import { defineStore } from 'pinia'

export const useStore = defineStore('app', {
  state: () => ({
    graphJSON: null
  }),
})
