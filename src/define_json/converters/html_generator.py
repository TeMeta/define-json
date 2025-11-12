"""
HTML Generation companion module for Define-JSON to Define-XML converter.

This module extends the high-fidelity DefineJSONToXMLConverter with HTML
generation capabilities, providing the best of both worlds:
- Perfect roundtrip XML generation from the core converter
- Human-readable HTML documentation via XSL transformation

Example usage:
    from json_to_xml import DefineJSONToXMLConverter
    from html_generator import DefineHTMLGenerator
    
    # Create HTML generator with high-fidelity converter
    generator = DefineHTMLGenerator()
    
    # Convert Define-JSON directly to HTML
    generator.json_to_htm(
        Path("study_define.json"),
        Path("study_define.html")
    )
    
    # Or convert existing Define-XML to HTML
    generator.xml_to_html(
        Path("study_define.xml"),
        Path("study_define.html")
    )
"""

from pathlib import Path
from typing import Optional, Dict, Any, Union
import tempfile
import logging
import json
from datetime import datetime

# Import the high-fidelity converter
try:
    from .json_to_xml import DefineJSONToXMLConverter
except ImportError:
    # Fallback if module structure is different
    import sys
    sys.path.append(str(Path(__file__).parent))
    from .json_to_xml import DefineJSONToXMLConverter

# Check for lxml availability
try:
    from lxml import etree
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False
    etree = None

logger = logging.getLogger(__name__)


class DefineHTMLGenerator:
    """
    HTML generation companion for DefineJSONToXMLConverter.
    
    Leverages the high-fidelity conversion from json_to_xml.py
    and adds HTML rendering capabilities for human-readable documentation.
    """
    
    def __init__(self, 
                 converter: Optional[DefineJSONToXMLConverter] = None,
                 default_xsl_path: Optional[Path] = None):
        """
        Initialize HTML generator.
        
        Args:
            converter: Optional converter instance. If not provided,
                      creates one with default settings.
            default_xsl_path: Default path to XSL stylesheet. If not provided,
                            will attempt to locate a bundled stylesheet.
        """
        self.converter = converter or DefineJSONToXMLConverter()
        self.default_xsl_path = default_xsl_path or self._find_default_xsl()
        
    def _find_default_xsl(self) -> Optional[Path]:
        """
        Attempt to locate a default XSL stylesheet.
        
        Searches in common locations:
        1. Same directory as this module
        2. Parent directory/stylesheets/
        3. Parent directory/data/
        4. Standard CDISC stylesheet locations
        """
        search_paths = [
            Path(__file__).parent / "define2-1.xsl",
            Path(__file__).parent / "stylesheets" / "define2-1.xsl",
            Path(__file__).parent.parent / "stylesheets" / "define2-1.xsl",
            Path(__file__).parent.parent / "data" / "define2-1.xsl",
            Path(__file__).parent.parent.parent / "data" / "define2-1.xsl",
            # Add more standard locations as needed
        ]
        
        for path in search_paths:
            if path.exists():
                logger.info(f"Found default XSL stylesheet at: {path}")
                return path
                
        logger.warning("No default XSL stylesheet found. You'll need to provide one.")
        return None
        
    def json_to_html(self, 
                    json_path: Union[Path, str], 
                    output_path: Union[Path, str], 
                    xsl_path: Optional[Union[Path, str]] = None,
                    keep_temp_xml: bool = False,
                    temp_xml_path: Optional[Union[Path, str]] = None) -> Dict[str, Any]:
        """
        Convert Define-JSON to HTML using the high-fidelity converter
        followed by XSL transformation.
        
        Args:
            json_path: Path to input Define-JSON file
            output_path: Path for output HTML file
            xsl_path: Optional path to XSL stylesheet (uses default if not provided)
            keep_temp_xml: If True, keeps the intermediate XML file
            temp_xml_path: Optional specific path for intermediate XML
            
        Returns:
            Dictionary with conversion results:
            {
                'success': bool,
                'html_path': Path to output HTML (if successful),
                'xml_path': Path to intermediate XML (if kept),
                'errors': List of error messages (if any),
                'warnings': List of warning messages (if any)
            }
            
        Benefits over old approach:
        - Uses perfect roundtrip XML generation
        - Preserves all namespace information
        - Maintains complete attribute fidelity
        - Provides detailed error reporting
        """
        result = {
            'success': False,
            'errors': [],
            'warnings': []
        }
        
        if not LXML_AVAILABLE:
            result['errors'].append(
                "lxml is required for HTML generation. Install with: pip install lxml"
            )
            return result
            
        # Convert paths to Path objects
        json_path = Path(json_path)
        output_path = Path(output_path)
        if xsl_path:
            xsl_path = Path(xsl_path)
        else:
            xsl_path = self.default_xsl_path
            
        if not xsl_path or not xsl_path.exists():
            result['errors'].append(
                f"XSL stylesheet not found: {xsl_path}. "
                "Please provide a valid XSL path."
            )
            return result
            
        if not json_path.exists():
            result['errors'].append(f"JSON file not found: {json_path}")
            return result
            
        try:
            # Determine XML output path
            if temp_xml_path:
                xml_path = Path(temp_xml_path)
                delete_xml = False
            elif keep_temp_xml:
                xml_path = output_path.with_suffix('.xml')
                delete_xml = False
            else:
                # Create temporary file
                with tempfile.NamedTemporaryFile(
                    mode='w', suffix='.xml', delete=False
                ) as tmp_xml:
                    xml_path = Path(tmp_xml.name)
                delete_xml = True
            
            # Step 1: Generate high-fidelity XML
            logger.info(f"Converting {json_path} to XML...")
            try:
                self.converter.convert_file(json_path, xml_path)
                logger.info(f"XML generated at: {xml_path}")
                if keep_temp_xml:
                    result['xml_path'] = xml_path
            except Exception as e:
                result['errors'].append(f"XML conversion failed: {str(e)}")
                if delete_xml and xml_path.exists():
                    xml_path.unlink()
                return result
            
            # Step 2: Apply XSL transformation
            logger.info(f"Applying XSL transformation...")
            html_result = self.xml_to_html(xml_path, output_path, xsl_path)
            
            if html_result['success']:
                result['success'] = True
                result['html_path'] = output_path
                logger.info(f"HTML generated successfully at: {output_path}")
            else:
                result['errors'].extend(html_result.get('errors', []))
                
            # Clean up temporary XML if needed
            if delete_xml and xml_path.exists():
                xml_path.unlink()
                
        except Exception as e:
            result['errors'].append(f"Unexpected error during HTML generation: {str(e)}")
            logger.error(f"HTML generation failed: {e}", exc_info=True)
            
        return result
    
    def xml_to_html(self, 
                   xml_path: Union[Path, str], 
                   output_path: Union[Path, str], 
                   xsl_path: Optional[Union[Path, str]] = None,
                   parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Convert Define-XML to HTML using XSL transformation.
        
        Args:
            xml_path: Path to input Define-XML file
            output_path: Path for output HTML file
            xsl_path: Optional path to XSL stylesheet (uses default if not provided)
            parameters: Optional dictionary of parameters to pass to XSL transformation
            
        Returns:
            Dictionary with conversion results:
            {
                'success': bool,
                'html_path': Path to output HTML (if successful),
                'errors': List of error messages (if any),
                'warnings': List of warning messages (if any),
                'xsl_messages': List of messages from XSL transformation
            }
        """
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'xsl_messages': []
        }
        
        if not LXML_AVAILABLE:
            result['errors'].append(
                "lxml is required for HTML generation. Install with: pip install lxml"
            )
            return result
            
        # Convert paths to Path objects
        xml_path = Path(xml_path)
        output_path = Path(output_path)
        if xsl_path:
            xsl_path = Path(xsl_path)
        else:
            xsl_path = self.default_xsl_path
            
        # Validate inputs
        if not xsl_path or not xsl_path.exists():
            result['errors'].append(
                f"XSL stylesheet not found: {xsl_path}. "
                "Please provide a valid XSL path."
            )
            return result
            
        if not xml_path.exists():
            result['errors'].append(f"XML file not found: {xml_path}")
            return result
            
        try:
            # Load XML document
            logger.info(f"Loading XML from: {xml_path}")
            xml_doc = etree.parse(str(xml_path))
            
            # Load XSL stylesheet
            logger.info(f"Loading XSL from: {xsl_path}")
            xsl_doc = etree.parse(str(xsl_path))
            
            # Create transformer with error handling
            transform = etree.XSLT(xsl_doc)
            
            # Apply transformation with optional parameters
            logger.info("Applying XSL transformation...")
            if parameters:
                # Convert parameters to XSLT-compatible format
                xslt_params = {}
                for key, value in parameters.items():
                    if isinstance(value, bool):
                        xslt_params[key] = "'true'" if value else "'false'"
                    elif isinstance(value, (int, float)):
                        xslt_params[key] = str(value)
                    else:
                        # String parameters need to be quoted for XSLT
                        xslt_params[key] = f"'{value}'"
                html_doc = transform(xml_doc, **xslt_params)
            else:
                html_doc = transform(xml_doc)
            
            # Capture any XSL messages
            if transform.error_log:
                for entry in transform.error_log:
                    message = f"{entry.message} (line {entry.line})"
                    if entry.level_name == 'ERROR':
                        result['errors'].append(message)
                    elif entry.level_name == 'WARNING':
                        result['warnings'].append(message)
                    else:
                        result['xsl_messages'].append(message)
            
            # Write HTML output
            logger.info(f"Writing HTML to: {output_path}")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(etree.tostring(
                    html_doc,
                    pretty_print=True,
                    method='html',
                    encoding='utf-8'
                ))
            
            result['success'] = True
            result['html_path'] = output_path
            logger.info("HTML generation completed successfully")
            
        except etree.XSLTParseError as e:
            result['errors'].append(f"XSL parse error: {str(e)}")
            logger.error(f"XSL parse error: {e}")
        except etree.XMLSyntaxError as e:
            result['errors'].append(f"XML syntax error: {str(e)}")
            logger.error(f"XML syntax error: {e}")
        except Exception as e:
            result['errors'].append(f"Unexpected error during transformation: {str(e)}")
            logger.error(f"XSL transformation failed: {e}", exc_info=True)
            
        return result
    
    def generate_preview(self, 
                        json_path: Union[Path, str],
                        max_datasets: int = 5,
                        max_variables: int = 10) -> str:
        """
        Generate a quick HTML preview of Define-JSON content.
        
        This method creates a simplified HTML view without requiring XSL transformation,
        useful for quick validation and review.
        
        Args:
            json_path: Path to Define-JSON file
            max_datasets: Maximum number of datasets to include in preview
            max_variables: Maximum number of variables per dataset
            
        Returns:
            HTML string containing the preview
        """
        json_path = Path(json_path)
        
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        # Build HTML preview
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '<meta charset="utf-8">',
            '<title>Define-JSON Preview</title>',
            '<style>',
            'body { font-family: Arial, sans-serif; margin: 20px; }',
            'h1 { color: #333; }',
            'h2 { color: #666; border-bottom: 2px solid #ddd; padding-bottom: 5px; }',
            'table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }',
            'th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }',
            'th { background-color: #f2f2f2; }',
            '.metadata { background-color: #f9f9f9; padding: 10px; margin-bottom: 20px; }',
            '</style>',
            '</head>',
            '<body>',
            '<h1>Define-JSON Preview</h1>',
        ]
        
        # Add metadata section
        html_parts.append('<div class="metadata">')
        html_parts.append('<h2>Study Metadata</h2>')
        html_parts.append('<table>')
        
        metadata_fields = [
            ('Study OID', data.get('studyOID', 'N/A')),
            ('Study Name', data.get('studyName', 'N/A')),
            ('Protocol Name', data.get('protocolName', 'N/A')),
            ('Creation DateTime', data.get('creationDateTime', 'N/A')),
        ]
        
        for label, value in metadata_fields:
            html_parts.append(f'<tr><th>{label}</th><td>{value}</td></tr>')
        html_parts.append('</table>')
        html_parts.append('</div>')
        
        # Add datasets preview
        datasets = data.get('itemGroups', [])[:max_datasets]
        if datasets:
            html_parts.append('<h2>Datasets Preview</h2>')
            for dataset in datasets:
                html_parts.append(f'<h3>{dataset.get("name", "Unknown Dataset")}</h3>')
                html_parts.append('<table>')
                html_parts.append('<tr><th>Variable</th><th>Label</th><th>Type</th></tr>')
                
                items = dataset.get('items', [])[:max_variables]
                for item in items:
                    # Try to find variable details
                    var_oid = item.get('OID') or item.get('itemOID')
                    var_info = self._find_variable_info(data, var_oid)
                    
                    html_parts.append('<tr>')
                    html_parts.append(f'<td>{var_info.get("name", var_oid)}</td>')
                    html_parts.append(f'<td>{var_info.get("label", "")}</td>')
                    html_parts.append(f'<td>{var_info.get("dataType", "")}</td>')
                    html_parts.append('</tr>')
                    
                if len(dataset.get('items', [])) > max_variables:
                    html_parts.append('<tr><td colspan="3"><em>... and more</em></td></tr>')
                    
                html_parts.append('</table>')
                
        html_parts.extend(['</body>', '</html>'])
        
        return '\n'.join(html_parts)
    
    def _find_variable_info(self, data: Dict[str, Any], var_oid: str) -> Dict[str, Any]:
        """Helper to find variable information by OID."""
        for item in data.get('items', []):
            if item.get('OID') == var_oid:
                return item
        return {'name': var_oid}
    
    def batch_convert(self, 
                     input_dir: Union[Path, str],
                     output_dir: Union[Path, str],
                     pattern: str = "*.json",
                     xsl_path: Optional[Union[Path, str]] = None) -> Dict[str, Any]:
        """
        Batch convert multiple Define-JSON files to HTML.
        
        Args:
            input_dir: Directory containing Define-JSON files
            output_dir: Directory for output HTML files
            pattern: File pattern to match (default: "*.json")
            xsl_path: Optional path to XSL stylesheet
            
        Returns:
            Dictionary with batch conversion results
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'files': []
        }
        
        for json_file in input_dir.glob(pattern):
            results['total'] += 1
            output_file = output_dir / json_file.with_suffix('.html').name
            
            file_result = {
                'input': json_file,
                'output': output_file
            }
            
            conversion_result = self.json_to_htm(
                json_file, output_file, xsl_path
            )
            
            if conversion_result['success']:
                results['successful'] += 1
                file_result['status'] = 'success'
            else:
                results['failed'] += 1
                file_result['status'] = 'failed'
                file_result['errors'] = conversion_result.get('errors', [])
                
            results['files'].append(file_result)
            
        return results


# Convenience function for quick conversion
def json_to_html(json_path: Union[Path, str], 
                 html_path: Union[Path, str],
                 xsl_path: Optional[Union[Path, str]] = None) -> bool:
    """
    Convenience function for quick JSON to HTML conversion.
    
    Args:
        json_path: Path to Define-JSON file
        html_path: Path for output HTML file
        xsl_path: Optional path to XSL stylesheet
        
    Returns:
        True if successful, False otherwise
    """
    generator = DefineHTMLGenerator()
    result = generator.convert_file(json_path, html_path, xsl_path)
    return result['success']


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python html_generator.py <input.json> <output.html> [stylesheet.xsl]")
        sys.exit(1)
        
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    xsl_file = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Perform conversion
    success = json_to_html(input_file, output_file, xsl_file)
    
    if success:
        print(f"Successfully converted {input_file} to {output_file}")
    else:
        print(f"Failed to convert {input_file}")
        sys.exit(1)
