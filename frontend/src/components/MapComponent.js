import React, { useEffect } from 'react';
import L from 'leaflet';
// Import map layout styles
import './styles/styles.css';

const MapComponent = ({ setMap }) => {
  useEffect(() => {
    // Check if the map is already initialized
    let map = L.map('map', { preferCanvas: true });

    // expose the map instance to the parent so other components can use it
    setMap(map);

    map.setView([51.505, -0.09], 13); // Change coordinates as needed

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    // Cleanup function to remove the map instance on unmount
    return () => {
      if (map) {
        map.remove();
      }
      // reset parent state when the component unmounts
      setMap(null);
    };
  }, [setMap]);

  return <div id="map" className="map"></div>;
};

export default MapComponent;
