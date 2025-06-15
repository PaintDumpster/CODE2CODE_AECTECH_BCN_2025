<template>
  <div ref="container" style="width: 100%; height: 100%; position: relative;"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as OBC from "@thatopen/components"
import * as THREE from "three"

const props = defineProps({ ifcFile: Object })

const container = ref(null)
let components = null
let world = null
let fragmentIfcLoader = null

onMounted(() => {
  // Initialize components
  components = new OBC.Components()
  const worlds = components.get(OBC.Worlds)
  world = worlds.create()

  // Set up scene
  world.scene = new OBC.SimpleScene(components)
  world.renderer = new OBC.SimpleRenderer(components, container.value)
  world.camera = new OBC.SimpleCamera(components)
  components.init()

  // Configure the renderer first
  world.renderer.three.outputColorSpace = THREE.SRGBColorSpace
  world.renderer.three.toneMapping = THREE.ACESFilmicToneMapping
  world.renderer.three.toneMappingExposure = 1

  // Set background color to white and add grid
  world.scene.three.background = new THREE.Color(0xffffff)
  const gridHelper = new THREE.GridHelper(1000, 100, 0x888888, 0xcccccc)
  world.scene.three.add(gridHelper)

  // Add ambient light with reduced intensity
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
  world.scene.three.add(ambientLight)

  // Add directional light with adjusted position and intensity
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5)
  directionalLight.position.set(1, 1, 1)
  world.scene.three.add(directionalLight)

  // Get the IFC loader
  fragmentIfcLoader = components.get(OBC.IfcLoader)
  fragmentIfcLoader.settings.webIfc.COORDINATE_TO_ORIGIN = true

  // Handle window resize
  const handleResize = () => {
    if (world.renderer) {
      world.renderer.resize()
    }
  }
  window.addEventListener('resize', handleResize)
})

watch(() => props.ifcFile, async (newFile) => {
  if (newFile && fragmentIfcLoader && world) {
    // Remove previous models
    while (world.scene.three.children.length > 1) {
      world.scene.three.remove(world.scene.three.children[1])
    }
    const buffer = await newFile.arrayBuffer()
    const model = await fragmentIfcLoader.load(new Uint8Array(buffer))
    model.name = newFile.name

    model.traverse((child) => {
      if (child.isMesh) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xcccccc,
          emissive: 0x444444,
          side: THREE.DoubleSide,
          flatShading: false,
          transparent: true,
          opacity: 0.8
        });
      }
    });

    world.scene.three.add(model)

    // Position camera to look at the model
    world.camera.controls.setPosition(10, 10, 10)
    world.camera.controls.setTarget(0, 0, 0)
  }
})

onUnmounted(() => {
  if (components) {
    components.dispose()
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
div {
  background-color: #f5f5f5;
}
</style> 