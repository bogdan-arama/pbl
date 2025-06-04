import React, { useEffect } from 'react';
import L from 'leaflet';
// Import map layout styles
import './styles/styles.css';

const MapComponent = ({ setMap }) => {
  useEffect(() => {
    // Check if the map is already initialized
    let map = L.map('map', { preferCanvas: true });

    map.setView([51.505, -0.09], 13); // Change coordinates as needed

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    // Cleanup function to remove the map instance on unmount
    return () => {
      if (map) {
        map.remove();
      }
    };
  }, [setMap]);

  return <div id="map" className="map"></div>;
};

export default MapComponent;
