import os
from pathlib import Path
from photogrammetry_processor import PhotogrammetryProcessor
from room_ontology import RoomOntology

def process_room_data(
    data_dir: str,
    point_cloud_file: str,
    camera_params_file: str,
    image_dir: str,
    output_dir: str
):
    """
    Process room data from photogrammetry outputs
    
    Args:
        data_dir: Base directory containing all data
        point_cloud_file: Path to point cloud file (.pcd or .ply)
        camera_params_file: Path to Metashape camera parameters
        image_dir: Directory containing images
        output_dir: Directory to save processed data
    """
    # Initialize processor
    processor = PhotogrammetryProcessor(data_dir)
    
    # Load data
    print("Loading point cloud...")
    point_cloud = processor.load_point_cloud(point_cloud_file)
    
    print("Loading camera parameters...")
    camera_params = processor.load_camera_params(camera_params_file)
    
    print("Loading images...")
    images = processor.load_images(image_dir)
    
    # Preprocess point cloud
    print("Preprocessing point cloud...")
    processed_cloud = processor.preprocess_point_cloud(
        voxel_size=0.02,  # Adjust based on your point cloud density
        remove_outliers=True
    )
    
    # Segment planes (walls, floor, ceiling)
    print("Segmenting planes...")
    planes = processor.segment_planes(
        distance_threshold=0.02,  # Adjust based on your point cloud scale
        ransac_n=3,
        num_iterations=1000
    )
    
    # Initialize ontology
    ontology = RoomOntology()
    
    # Add room and its components to ontology
    print("Creating knowledge graph...")
    
    # Add room
    ontology.add_physical_object("room1", ontology.ROOM.Room, {
        "hasHeight": 3.0,  # Example value, should be calculated from point cloud
        "hasWidth": 4.0,   # Example value, should be calculated from point cloud
        "hasDepth": 5.0    # Example value, should be calculated from point cloud
    })
    
    # Add walls (from segmented planes)
    for i, plane in enumerate(planes):
        # Calculate plane dimensions and orientation
        # This is a simplified example - you'll need to implement proper calculations
        ontology.add_physical_object(f"wall{i+1}", ontology.ROOM.Wall, {
            "hasHeight": 3.0,  # Example value
            "hasWidth": 4.0,   # Example value
            "hasMaterial": "concrete"  # Example value, should be inferred from images
        })
        # Add spatial relationship
        ontology.add_spatial_relation(f"wall{i+1}", "isPartOf", "room1")
    
    # Save processed data
    print("Saving processed data...")
    processor.save_processed_data(output_dir)
    
    # Save ontology
    ontology.save(os.path.join(output_dir, "room_ontology.ttl"))
    
    print("Processing complete!")

if __name__ == "__main__":
    # Example usage
    data_dir = "data"
    point_cloud_file = "data/room.ply"
    camera_params_file = "data/cameras.json"
    image_dir = "data/images"
    output_dir = "data/processed"
    
    process_room_data(
        data_dir=data_dir,
        point_cloud_file=point_cloud_file,
        camera_params_file=camera_params_file,
        image_dir=image_dir,
        output_dir=output_dir
    ) 