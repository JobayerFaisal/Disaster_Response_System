import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

export default function MapView({ flood, routes }) {
  const mapContainer = useRef(null);
  const map = useRef(null);

  // initial map setup
  useEffect(() => {
    if (map.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://demotiles.maplibre.org/style.json",
      center: [90.4125, 23.8103],
      zoom: 11,
    });

    map.current.addControl(new maplibregl.NavigationControl());
  }, []);

  // update flood polygons
  useEffect(() => {
    if (!map.current || !flood) return;

    const id = "flood-layer";

    if (map.current.getSource(id)) {
      map.current.getSource(id).setData(flood.geojson);
    } else {
      map.current.addSource(id, {
        type: "geojson",
        data: flood.geojson,
      });

      map.current.addLayer({
        id,
        type: "fill",
        source: id,
        paint: {
          "fill-color": [
            "match",
            ["get", "risk"],
            "RED", "#ff0000aa",
            "YELLOW", "#ffff00aa",
            "GREEN", "#00ff00aa",
            "#0000ffaa",
          ],
          "fill-opacity": 0.4,
        },
      });
    }
  }, [flood]);

  // update routes
  useEffect(() => {
    if (!map.current || !routes) return;

    const id = "route-layer";

    const geo = {
      type: "FeatureCollection",
      features: routes.map((r) => ({
        type: "Feature",
        geometry: {
          type: "LineString",
          coordinates: r.route.map((p) => p.split(",").map(Number)),
        },
        properties: {},
      })),
    };

    if (map.current.getSource(id)) {
      map.current.getSource(id).setData(geo);
    } else {
      map.current.addSource(id, { type: "geojson", data: geo });

      map.current.addLayer({
        id,
        type: "line",
        source: id,
        paint: {
          "line-color": "#00aaff",
          "line-width": 4,
        },
      });
    }
  }, [routes]);

  return (
    <div className="w-full h-[500px] border rounded-lg overflow-hidden">
      <div ref={mapContainer} className="w-full h-full" />
    </div>
  );
}

