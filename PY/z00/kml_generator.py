import xml.etree.ElementTree as ET
from typing import List, Tuple
import time

class KMLGenerator:
    """Generates a privacy-first intent_world.kml for planetary visualization."""
    def __init__(self, name: str = "Σ-Intent World"):
        self.kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        self.document = ET.SubElement(self.kml, "Document")
        ET.SubElement(self.document, "name").text = name
        
        # Styles
        self._add_styles()

    def _add_styles(self):
        # Resonance Style (Glow)
        style = ET.SubElement(self.document, "Style", id="resonance_style")
        line = ET.SubElement(style, "LineStyle")
        ET.SubElement(line, "color").text = "ff00ffff" # Cyan
        ET.SubElement(line, "width").text = "4"
        poly = ET.SubElement(style, "PolyStyle")
        ET.SubElement(poly, "color").text = "8800ffff" # Translucent Cyan
        ET.SubElement(poly, "fill").text = "1"
        ET.SubElement(poly, "outline").text = "1"

        # Antenna Style (3D Building)
        style = ET.SubElement(self.document, "Style", id="antenna_style")
        poly = ET.SubElement(style, "PolyStyle")
        ET.SubElement(poly, "color").text = "aa00ffff" # Glassy Cyan
        ET.SubElement(poly, "fill").text = "1"
        ET.SubElement(poly, "outline").text = "1"

        # Pain Style (Discrepancy)
        style = ET.SubElement(self.document, "Style", id="pain_style")
        icon = ET.SubElement(style, "IconStyle")
        ET.SubElement(icon, "color").text = "ff0000ff" # Red
        ET.SubElement(icon, "scale").text = "1.2"

    def add_placemark(self, name: str, lat: float, lon: float, height: float = 0, 
                      style: str = "#resonance_style", description: str = ""):
        """Adds a localized frequency point."""
        pm = ET.SubElement(self.document, "Placemark")
        if name: ET.SubElement(pm, "name").text = name
        if description: ET.SubElement(pm, "description").text = description
        ET.SubElement(pm, "styleUrl").text = style
        
        point = ET.SubElement(pm, "Point")
        ET.SubElement(point, "extrude").text = "1"
        ET.SubElement(point, "altitudeMode").text = "relativeToGround"
        ET.SubElement(point, "coordinates").text = f"{lon},{lat},{height}"

    def add_extruded_polygon(self, coords: List[Tuple[float, float]], height: float, 
                             name: str = "", style: str = "#antenna_style"):
        """Adds a 3D building-as-antenna."""
        pm = ET.SubElement(self.document, "Placemark")
        if name: ET.SubElement(pm, "name").text = name
        ET.SubElement(pm, "styleUrl").text = style
        
        poly = ET.SubElement(pm, "Polygon")
        ET.SubElement(poly, "extrude").text = "1"
        ET.SubElement(poly, "altitudeMode").text = "relativeToGround"
        boundary = ET.SubElement(poly, "outerBoundaryIs")
        ring = ET.SubElement(boundary, "LinearRing")
        
        coord_str = " ".join([f"{lon},{lat},{height}" for lat, lon in coords])
        ET.SubElement(ring, "coordinates").text = coord_str

    def add_path(self, coords: List[Tuple[float, float]], name: str = "", 
                 style: str = "#resonance_style", height: float = 10):
        """Adds a street-as-data-bus path."""
        pm = ET.SubElement(self.document, "Placemark")
        if name: ET.SubElement(pm, "name").text = name
        ET.SubElement(pm, "styleUrl").text = style
        
        line = ET.SubElement(pm, "LineString")
        ET.SubElement(line, "extrude").text = "0"
        ET.SubElement(line, "tessellate").text = "1"
        ET.SubElement(line, "altitudeMode").text = "relativeToGround"
        
        coord_str = " ".join([f"{lon},{lat},{height}" for lat, lon in coords])
        ET.SubElement(line, "coordinates").text = coord_str

    def build_membrane(self, filename: str):
        tree = ET.ElementTree(self.kml)
        with open(filename, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)
        print(f"✅ KML Membrane materialized: {filename}")

def test_kml_v01():
    print("🌐 Testing Gateway KML v0.1...")
    gen = KMLGenerator()
    
    # Simulate a few resonance points (e.g. Dnieper Delta)
    # Latitude/Longitude for Kherson/Delta area
    gen.add_placemark("Resonance-High", 46.63, 32.61, 5000)
    gen.add_placemark("Resonance-Mid", 46.5, 32.2, 2500)
    
    # Simulate a Pain Marker (Doctor)
    gen.add_placemark("PAIN-DISCREPANCY", 46.7, 32.8, 1000, style="#pain_style", 
                      description="Trace Mismatch: Expected sediment, found void.")

    gen.build_membrane("output.kml")

if __name__ == "__main__":
    test_kml_v01()
