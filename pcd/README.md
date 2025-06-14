# Room Ontology and Semantic Enrichment

This project implements a semantic enrichment pipeline for indoor spaces using point cloud data. It creates a knowledge graph representation of rooms and their contents using ontologies.

## Project Structure

```
pcd/
├── ontology/         # Ontology definitions and schema
├── src/             # Source code
├── data/            # Input/output data
└── notebooks/       # Jupyter notebooks for analysis
```

## Features

1. Room Ontology
   - Custom domain ontology for indoor spaces
   - Aligned with CIDOC-CRM, GeoSPARQL, and BOT
   - Core classes for physical objects, spatial locations, and relationships

2. Point Cloud Processing
   - Input: .pcd/.ply files or 3D meshes
   - Segmentation using clustering and primitive fitting
   - Object detection and classification

3. Semantic Enrichment
   - Object classification
   - Material inference
   - Spatial relationship extraction
   - Optional text-based annotations

4. Knowledge Graph
   - RDF-based representation
   - SPARQL querying
   - Visualization capabilities

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Define your room ontology:
```python
from src.room_ontology import RoomOntology

ontology = RoomOntology()
```

2. Add objects and relationships:
```python
ontology.add_physical_object("chair1", ontology.ROOM.Furniture, {
    "hasMaterial": "wood",
    "hasHeight": 0.8
})
```

3. Query the knowledge graph:
```python
results = ontology.query("""
    SELECT ?obj ?material
    WHERE {
        ?obj room:hasMaterial ?material .
    }
""")
```

## Dependencies

- RDFLib: Ontology and graph management
- Open3D: Point cloud processing
- PyTorch: Deep learning for object detection
- scikit-learn: Clustering and segmentation
- Other utilities: numpy, scipy, matplotlib, pandas 