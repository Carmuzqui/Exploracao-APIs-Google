"""
App de Teste: Integração ArcGIS 3D no Streamlit (Sem Login / Open Source Basemap)
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ArcGIS 3D Eletropostos", layout="wide")

st.title("🌍 Teste de integração ArcGIS 3D")

arcgis_html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no">
  <title>ArcGIS 3D - Eletropostos</title>
  <style>
    html, body, #viewDiv {
      padding: 0;
      margin: 0;
      height: 100vh;
      width: 100%;
      background-color: #121212;
    }
  </style>
  
  <link rel="stylesheet" href="https://js.arcgis.com/4.28/esri/themes/light/main.css">
  <script src="https://js.arcgis.com/4.28/"></script>

  <script>
    require([
      "esri/Map",
      "esri/views/SceneView",
      "esri/Graphic",
      "esri/layers/GraphicsLayer"
    ], function(Map, SceneView, Graphic, GraphicsLayer) {

      // "osm" (OpenStreetMap) público
      const map = new Map({
        basemap: "osm" 
        
      });

      const view = new SceneView({
        container: "viewDiv",
        map: map,
        camera: {
          position: {
            x: -46.6333,
            y: -23.6500, 
            z: 5000      
          },
          tilt: 60,      
          heading: 0
        }
      });

      const graphicsLayer = new GraphicsLayer();
      map.add(graphicsLayer);

      const point = {
        type: "point",
        longitude: -46.6333,
        latitude: -23.5505
      };

      // Eletroposto em 3D
      const evSymbol3D = {
        type: "point-3d",
        symbolLayers: [{
          type: "object",
          width: 150,   
          height: 400,  
          depth: 150,   
          resource: { primitive: "cylinder" },
          material: { color: [0, 100, 255, 0.8] } // Azul translúcido para que se destaque no mapa claro
        }]
      };

      const pointGraphic = new Graphic({
        geometry: point,
        symbol: evSymbol3D,
        attributes: {
            Name: "Eletroposto Piloto SP",
            Conectores: 4,
            Potencia: "150 kW",
            Distancia: "0 km"
        },
        popupTemplate: {
            title: "{Name}",
            content: "<b>Potência Máxima:</b> {Potencia}<br><b>Conectores:</b> {Conectores}<br><b>Status:</b> Operacional"
        }
      });

      graphicsLayer.add(pointGraphic);
    });
  </script>
</head>
<body>
  <div id="viewDiv"></div>
</body>
</html>
"""

components.html(arcgis_html, height=700)
