import { useEffect } from 'react';
import L from 'leaflet';

const EarthquakeAnimator = ({ map }) => {
  useEffect(() => {
    if (!map) return;

    const handleDoubleClick = (e) => {
      const { latlng } = e;

      const circle = L.circle(latlng, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 50000,
      }).addTo(map);

      let grow = true;
      let radius = 50000;

      const animation = setInterval(() => {
        if (grow) {
          radius += 10000;
          if (radius >= 100000) grow = false;
        } else {
          radius -= 10000;
          if (radius <= 50000) grow = true;
        }
        circle.setRadius(radius);
      }, 200);

      setTimeout(() => {
        clearInterval(animation);
        map.removeLayer(circle);
      }, 3000); // remove after 3 sec
    };

    map.on('dblclick', handleDoubleClick);

    return () => {
      map.off('dblclick', handleDoubleClick);
    };
  }, [map]);

  return null;
};

export default EarthquakeAnimator;
