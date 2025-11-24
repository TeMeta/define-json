"""
Cube Configuration Converter
Bridges between human-friendly YAML cube configs and formal define.py schema objects
"""

import yaml
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

from ..schema.define import (
    Item,
    DataStructureDefinition,
    CubeComponent,
    Dimension,
    Measure,
    DataAttribute,
    DataType
)


class CubeConfigConverter:
    """
    Converts between YAML cube configurations and define.py schema objects.
    
    Handles impedance mismatches:
    - Field names: id ↔ OID
    - DataType enums: string ↔ text
    - Structure: flat dicts ↔ typed objects
    - Component roles: role field ↔ Dimension/Measure/Attribute classes
    """
    
    # Mapping between YAML-friendly and schema enum values
    DATATYPE_YAML_TO_SCHEMA = {
        'string': DataType.text,
        'integer': DataType.integer,
        'float': DataType.float,
        'double': DataType.double,
        'date': DataType.date,
        'time': DataType.time,
        'datetime': DataType.datetime,
        'boolean': DataType.boolean,
    }
    
    DATATYPE_SCHEMA_TO_YAML = {v: k for k, v in DATATYPE_YAML_TO_SCHEMA.items()}
    # Special case: prefer 'string' over 'text' in YAML
    DATATYPE_SCHEMA_TO_YAML[DataType.text] = 'string'
    
    @classmethod
    def load_yaml_config(cls, config_path: str) -> Dict[str, Any]:
        """Load a YAML cube configuration file"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    @classmethod
    def yaml_to_schema(
        cls, 
        config: Dict[str, Any]
    ) -> Tuple[Dict[str, Item], Dict[str, CubeComponent], DataStructureDefinition]:
        """
        Convert YAML cube config to schema objects.
        
        Args:
            config: YAML config dict
            
        Returns:
            Tuple of (items_dict, components_dict, dsd)
            - items_dict: {item_id: Item object}
            - components_dict: {component_id: Dimension/Measure/Attribute object}
            - dsd: DataStructureDefinition object
        """
        # Convert items
        items_dict = {}
        yaml_items = config.get('items', {})
        for item_id, yaml_item in yaml_items.items():
            items_dict[item_id] = cls._yaml_item_to_schema(yaml_item)
        
        # Convert components based on role
        components_dict = {}
        yaml_components = config.get('components', {})
        for comp_id, yaml_comp in yaml_components.items():
            components_dict[comp_id] = cls._yaml_component_to_schema(yaml_comp)
        
        # Convert DSD
        yaml_dsd = config.get('data_structure_definition', {})
        dsd = cls._yaml_dsd_to_schema(yaml_dsd)
        
        return items_dict, components_dict, dsd
    
    @classmethod
    def _yaml_item_to_schema(cls, yaml_item: Dict[str, Any]) -> Item:
        """Convert a YAML item to an Item schema object"""
        # Map dataType
        datatype_str = yaml_item.get('dataType', 'string')
        datatype = cls.DATATYPE_YAML_TO_SCHEMA.get(datatype_str, DataType.text)
        
        # Build Item - handle optional fields
        item_kwargs = {
            'OID': yaml_item['id'],  # id → OID
            'name': yaml_item['name'],
        }
        
        # Optional fields
        if 'label' in yaml_item:
            item_kwargs['label'] = yaml_item['label']
        if 'description' in yaml_item:
            item_kwargs['description'] = yaml_item['description']
        
        item_kwargs['dataType'] = datatype
        
        # Handle extended attributes (length, units) as extensions
        # For now, store in description if not already present
        extra_notes = []
        if 'length' in yaml_item:
            extra_notes.append(f"Length: {yaml_item['length']}")
        if 'units' in yaml_item:
            extra_notes.append(f"Units: {yaml_item['units']}")
        
        if extra_notes:
            desc = item_kwargs.get('description', '')
            if desc:
                desc += ' | ' + ' | '.join(extra_notes)
            else:
                desc = ' | '.join(extra_notes)
            item_kwargs['description'] = desc
        
        return Item(**item_kwargs)
    
    @classmethod
    def _yaml_component_to_schema(cls, yaml_comp: Dict[str, Any]) -> CubeComponent:
        """Convert a YAML component to appropriate CubeComponent subclass"""
        role = yaml_comp.get('role', 'attribute').lower()
        
        comp_kwargs = {
            'OID': yaml_comp['id'],  # id → OID
            'name': yaml_comp['name'],
            'item': yaml_comp['item'],  # Item reference
        }
        
        if 'description' in yaml_comp:
            comp_kwargs['description'] = yaml_comp['description']
        
        # Create appropriate subclass based on role
        if role == 'dimension':
            return Dimension(**comp_kwargs)
        elif role == 'measure':
            return Measure(**comp_kwargs)
        elif role == 'attribute':
            return DataAttribute(**comp_kwargs)
        else:
            raise ValueError(f"Unknown component role: {role}")
    
    @classmethod
    def _yaml_dsd_to_schema(cls, yaml_dsd: Dict[str, Any]) -> DataStructureDefinition:
        """Convert a YAML DSD to DataStructureDefinition schema object"""
        dsd_kwargs = {
            'OID': yaml_dsd['id'],  # id → OID
            'name': yaml_dsd['name'],
        }
        
        if 'description' in yaml_dsd:
            dsd_kwargs['description'] = yaml_dsd['description']
        
        # Lists of component OID references
        if 'dimensions' in yaml_dsd:
            dsd_kwargs['dimensions'] = yaml_dsd['dimensions']
        if 'measures' in yaml_dsd:
            dsd_kwargs['measures'] = yaml_dsd['measures']
        if 'attributes' in yaml_dsd:
            dsd_kwargs['attributes'] = yaml_dsd['attributes']
        
        return DataStructureDefinition(**dsd_kwargs)
    
    @classmethod
    def schema_to_yaml(
        cls,
        items_dict: Dict[str, Item],
        components_dict: Dict[str, CubeComponent],
        dsd: DataStructureDefinition,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Convert schema objects back to YAML cube config format.
        
        Args:
            items_dict: {item_id: Item object}
            components_dict: {component_id: CubeComponent object}
            dsd: DataStructureDefinition object
            include_metadata: Include name/description at top level
            
        Returns:
            Dict suitable for YAML serialization
        """
        config = {}
        
        if include_metadata:
            config['name'] = dsd.name or "Data Cube Configuration"
            config['description'] = dsd.description or "Generated from schema objects"
        
        # Convert items
        config['items'] = {}
        for item_id, item in items_dict.items():
            config['items'][item_id] = cls._schema_item_to_yaml(item)
        
        # Convert components
        config['components'] = {}
        for comp_id, comp in components_dict.items():
            config['components'][comp_id] = cls._schema_component_to_yaml(comp)
        
        # Convert DSD
        config['data_structure_definition'] = cls._schema_dsd_to_yaml(dsd)
        
        return config
    
    @classmethod
    def _schema_item_to_yaml(cls, item: Item) -> Dict[str, Any]:
        """Convert an Item schema object to YAML format"""
        yaml_item = {
            'id': item.OID,  # OID → id
            'name': item.name,
        }
        
        if item.label:
            yaml_item['label'] = item.label
        
        # Map dataType back
        if item.dataType:
            yaml_item['dataType'] = cls.DATATYPE_SCHEMA_TO_YAML.get(
                item.dataType, 
                str(item.dataType.value) if hasattr(item.dataType, 'value') else str(item.dataType)
            )
        
        if item.description:
            # Try to extract length/units from description if they were embedded
            desc = item.description
            # Simple extraction (this is lossy, ideally store in Item extensions)
            if ' | Length: ' in desc:
                parts = desc.split(' | ')
                clean_desc = parts[0]
                for part in parts[1:]:
                    if part.startswith('Length: '):
                        yaml_item['length'] = int(part.split(': ')[1])
                    elif part.startswith('Units: '):
                        yaml_item['units'] = part.split(': ')[1]
                    else:
                        clean_desc += ' | ' + part
                yaml_item['description'] = clean_desc
            else:
                yaml_item['description'] = desc
        
        return yaml_item
    
    @classmethod
    def _schema_component_to_yaml(cls, comp: CubeComponent) -> Dict[str, Any]:
        """Convert a CubeComponent schema object to YAML format"""
        yaml_comp = {
            'id': comp.OID,  # OID → id
            'name': comp.name,
            'item': comp.item,  # Item reference
        }
        
        # Determine role from class type
        if isinstance(comp, Dimension):
            yaml_comp['role'] = 'dimension'
        elif isinstance(comp, Measure):
            yaml_comp['role'] = 'measure'
        elif isinstance(comp, DataAttribute):
            yaml_comp['role'] = 'attribute'
        
        if comp.description:
            yaml_comp['description'] = comp.description
        
        return yaml_comp
    
    @classmethod
    def _schema_dsd_to_yaml(cls, dsd: DataStructureDefinition) -> Dict[str, Any]:
        """Convert a DataStructureDefinition schema object to YAML format"""
        yaml_dsd = {
            'id': dsd.OID,  # OID → id
            'name': dsd.name,
        }
        
        if dsd.description:
            yaml_dsd['description'] = dsd.description
        
        if dsd.dimensions:
            yaml_dsd['dimensions'] = dsd.dimensions
        if dsd.measures:
            yaml_dsd['measures'] = dsd.measures
        if dsd.attributes:
            yaml_dsd['attributes'] = dsd.attributes
        
        return yaml_dsd
    
    @classmethod
    def validate_and_convert(cls, config_path: str) -> Tuple[Dict[str, Item], Dict[str, CubeComponent], DataStructureDefinition]:
        """
        Load YAML config, convert to schema, and validate.
        
        This is the main entry point for users.
        
        Args:
            config_path: Path to YAML cube config
            
        Returns:
            Tuple of validated (items_dict, components_dict, dsd)
            
        Raises:
            ValidationError if schema validation fails
        """
        config = cls.load_yaml_config(config_path)
        items_dict, components_dict, dsd = cls.yaml_to_schema(config)
        
        # Validation happens automatically via Pydantic
        # If we get here, all objects are valid
        
        return items_dict, components_dict, dsd
    
    @classmethod
    def save_yaml_config(cls, config: Dict[str, Any], output_path: str) -> None:
        """Save config dict to YAML file"""
        with open(output_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

