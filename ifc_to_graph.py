# IFC to GraphML Converter

# This script converts IFC files to GraphML format, preserving the building element relationships.
# It will automatically process any .ifc file found in the data folder.

# To run just type "python ifc_to_graph.py" in the terminal



import ifcopenshell
import networkx as nx
from typing import Dict, Any
import argparse
import os
import glob

def extract_properties(entity):
    """Extracts general properties and quantities from an IFC entity."""
    data = {
        "GlobalId": entity.GlobalId,
        "Name": entity.Name,
        "Description": getattr(entity, "Description", None),
        "ObjectType": getattr(entity, "ObjectType", None),
        "IfcType": entity.is_a()
    }

    if data["Name"] is None and hasattr(entity, "IsDefinedBy"):
        for rel in entity.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties") and hasattr(rel, "RelatingPropertyDefinition"):
                prop_def = rel.RelatingPropertyDefinition
                if prop_def.is_a("IfcPropertySet"):
                    if prop_def.Name == "Pset_SpaceCommon":
                        for prop in prop_def.HasProperties:
                            if prop.is_a("IfcPropertySingleValue") and prop.Name == "Name":
                                data["Name"] = getattr(prop.NominalValue, "wrappedValue", None)
                                break
                    else:
                        for prop in prop_def.HasProperties:
                            if prop.is_a("IfcPropertySingleValue"):
                                if prop.Name in ["Name", "name", "LongName", "longname"]:
                                    data["Name"] = getattr(prop.NominalValue, "wrappedValue", None)
                                    break
                                property_value = getattr(prop.NominalValue, "wrappedValue", None)
                                if property_value in ["Name", "LongName"]:
                                    for inner_prop in prop_def.HasProperties:
                                        if inner_prop.is_a("IfcPropertySingleValue") and inner_prop.Name == property_value:
                                            data["Name"] = getattr(inner_prop.NominalValue, "wrappedValue", None)
                                            break
                                    break

    if data["Name"] is None and hasattr(entity, 'LongName'):
        data["Name"] = entity.LongName

    return data

def ifc_to_graphml(ifc_file_path: str, output_path: str):
    """Convert IFC file to GraphML format.
    
    Args:
        ifc_file_path: Path to the IFC file
        output_path: Path where the GraphML file will be saved
    """
    # Load IFC file
    ifc_file = ifcopenshell.open(ifc_file_path)
    
    # Create graph
    G = nx.Graph()
    
    # Add Rooms
    rooms = ifc_file.by_type("IfcSpace")
    for room in rooms:
        room_id = room.GlobalId
        G.add_node(room_id, **extract_properties(room), category="IfcSpace")
    
    # Add Room-Element Connections
    space_boundaries = ifc_file.by_type("IfcRelSpaceBoundary")
    for rel in space_boundaries:
        room = rel.RelatingSpace
        element = rel.RelatedBuildingElement
        if room and element:
            if element.GlobalId not in G.nodes:
                G.add_node(element.GlobalId, **extract_properties(element), category=element.is_a())
            G.add_edge(room.GlobalId, element.GlobalId, relation="SURROUNDS")
    
    # Add Wall-Window/Door Connections
    for rel in ifc_file.by_type("IfcRelVoidsElement"):
        wall = rel.RelatingBuildingElement
        opening = rel.RelatedOpeningElement
        
        for fill_rel in ifc_file.by_type("IfcRelFillsElement"):
            if fill_rel.RelatingOpeningElement == opening:
                filled_element = fill_rel.RelatedBuildingElement
                if (
                    wall
                    and filled_element
                    and "Wall" in wall.is_a()
                    and filled_element.is_a() in ["IfcDoor", "IfcWindow"]
                ):
                    if wall.GlobalId not in G.nodes:
                        G.add_node(wall.GlobalId, **extract_properties(wall), category=wall.is_a())
                    if filled_element.GlobalId not in G.nodes:
                        G.add_node(filled_element.GlobalId, **extract_properties(filled_element), category=filled_element.is_a())
                    G.add_edge(wall.GlobalId, filled_element.GlobalId, relation="VOIDS")
    
    # Remove unconnected nodes
    unconnected_nodes = [node for node, degree in G.degree() if degree == 0]
    G.remove_nodes_from(unconnected_nodes)
    
    # Convert node attributes to strings to ensure compatibility
    for node in G.nodes():
        for key, value in G.nodes[node].items():
            if not isinstance(value, (str, int, float, bool)):
                G.nodes[node][key] = str(value)
    
    # Convert edge attributes to strings
    for u, v, data in G.edges(data=True):
        for key, value in data.items():
            if not isinstance(value, (str, int, float, bool)):
                data[key] = str(value)
    
    # Export to GraphML
    nx.write_graphml(G, output_path)
    print(f"Graph exported to {output_path}")
    return G

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert IFC files to GraphML format')
    parser.add_argument('--input-dir', '-i', default='data',
                      help='Directory containing IFC files (default: data)')
    parser.add_argument('--output-dir', '-o', default='data',
                      help='Directory for output GraphML files (default: data)')
    
    args = parser.parse_args()
    
    # Check if input directory exists
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist")
        return
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Find all .ifc files in the input directory
    ifc_files = glob.glob(os.path.join(args.input_dir, "*.ifc"))
    
    if not ifc_files:
        print(f"No .ifc files found in {args.input_dir}")
        return
    
    # Process each IFC file
    for ifc_path in ifc_files:
        try:
            # Generate output path by replacing .ifc with .graphml
            output_path = os.path.join(
                args.output_dir,
                os.path.splitext(os.path.basename(ifc_path))[0] + '.graphml'
            )
            
            print(f"\nProcessing: {ifc_path}")
            ifc_to_graphml(ifc_path, output_path)
            print(f"Successfully converted to: {output_path}")
            
        except Exception as e:
            print(f"Error processing {ifc_path}: {str(e)}")

if __name__ == "__main__":
    main()
    