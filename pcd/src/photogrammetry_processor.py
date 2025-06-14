import os
import numpy as np
import open3d as o3d
from pathlib import Path
import json
from typing import Dict, List, Tuple, Optional

class PhotogrammetryProcessor:
    def __init__(self, data_dir: str):
        """
        Initialize the photogrammetry processor
        
        Args:
            data_dir: Directory containing photogrammetry data
        """
        self.data_dir = Path(data_dir)
        self.point_cloud = None
        self.camera_params = None
        self.images = {}
        
    def load_point_cloud(self, file_path: str) -> o3d.geometry.PointCloud:
        """
        Load point cloud from .pcd or .ply file
        
        Args:
            file_path: Path to point cloud file
            
        Returns:
            Open3D point cloud object
        """
        file_path = Path(file_path)
        if file_path.suffix.lower() == '.pcd':
            self.point_cloud = o3d.io.read_point_cloud(str(file_path))
        elif file_path.suffix.lower() == '.ply':
            self.point_cloud = o3d.io.read_point_cloud(str(file_path))
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
        return self.point_cloud
    
    def load_camera_params(self, metashape_file: str) -> Dict:
        """
        Load camera parameters from Metashape export
        
        Args:
            metashape_file: Path to Metashape camera parameters file
            
        Returns:
            Dictionary containing camera parameters
        """
        # This is a placeholder - actual implementation will depend on Metashape export format
        # You might need to parse XML, JSON, or other format depending on how you exported from Metashape
        with open(metashape_file, 'r') as f:
            self.camera_params = json.load(f)
        return self.camera_params
    
    def load_images(self, image_dir: str) -> Dict[str, np.ndarray]:
        """
        Load images from directory
        
        Args:
            image_dir: Directory containing images
            
        Returns:
            Dictionary mapping image names to numpy arrays
        """
        image_dir = Path(image_dir)
        for img_file in image_dir.glob('*.jpg'):
            # You might want to use PIL or cv2 for actual image loading
            # This is a placeholder
            self.images[img_file.name] = None
        return self.images
    
    def preprocess_point_cloud(self, 
                             voxel_size: float = 0.02,
                             remove_outliers: bool = True) -> o3d.geometry.PointCloud:
        """
        Preprocess point cloud data
        
        Args:
            voxel_size: Size of voxel for downsampling
            remove_outliers: Whether to remove statistical outliers
            
        Returns:
            Processed point cloud
        """
        if self.point_cloud is None:
            raise ValueError("No point cloud loaded")
            
        # Downsample point cloud
        downsampled = self.point_cloud.voxel_down_sample(voxel_size)
        
        if remove_outliers:
            # Remove statistical outliers
            cl, ind = downsampled.remove_statistical_outlier(
                nb_neighbors=20,
                std_ratio=2.0
            )
            downsampled = downsampled.select_by_index(ind)
            
        # Estimate normals
        downsampled.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
        )
        
        self.point_cloud = downsampled
        return self.point_cloud
    
    def segment_planes(self, 
                      distance_threshold: float = 0.02,
                      ransac_n: int = 3,
                      num_iterations: int = 1000) -> List[o3d.geometry.PointCloud]:
        """
        Segment planes from point cloud using RANSAC
        
        Args:
            distance_threshold: Maximum distance from point to plane
            ransac_n: Number of points to sample for RANSAC
            num_iterations: Number of RANSAC iterations
            
        Returns:
            List of point clouds, each representing a plane
        """
        if self.point_cloud is None:
            raise ValueError("No point cloud loaded")
            
        planes = []
        remaining_points = self.point_cloud
        
        while len(remaining_points.points) > ransac_n:
            # Find the largest plane
            plane_model, inliers = remaining_points.segment_plane(
                distance_threshold=distance_threshold,
                ransac_n=ransac_n,
                num_iterations=num_iterations
            )
            
            if len(inliers) < ransac_n:
                break
                
            # Extract the plane
            plane = remaining_points.select_by_index(inliers)
            planes.append(plane)
            
            # Remove the plane from remaining points
            remaining_points = remaining_points.select_by_index(inliers, invert=True)
            
        return planes
    
    def save_processed_data(self, output_dir: str):
        """
        Save processed data to output directory
        
        Args:
            output_dir: Directory to save processed data
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.point_cloud is not None:
            o3d.io.write_point_cloud(
                str(output_dir / "processed_point_cloud.ply"),
                self.point_cloud
            )
            
        if self.camera_params is not None:
            with open(output_dir / "camera_params.json", 'w') as f:
                json.dump(self.camera_params, f, indent=2) 