import React, { useState } from 'react';
import MapComponent from './MapComponent';
import EarthquakeAnimator from './EarthquakeAnimator';

const InteractiveMap = () => {
  const [map, setMap] = useState(null);

  return (
    <>
      <MapComponent setMap={setMap} />
      {map && <EarthquakeAnimator map={map} />}
    </>
  );
};

export default InteractiveMap;
