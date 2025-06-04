import React from 'react';
// Import component specific styles
import './styles/styles.css';

const InfoComponent = () => {
  const updateValue = (el) => {
    const value = el.value;
    const span = el.nextElementSibling;
    span.textContent = value;
  };

  return (
    <div className="info">
      <div className="Title">
        <div className="Logo"><img className="LogoImage" src="/Logo.png" alt="Logo" /></div>
        <div className="Name"><p className="NameApp">QuakeGen</p></div>
      </div>
      <div className="Numbers">
        <div className="Magnitude">
          <strong><h4 className="Text">Magnitude</h4></strong>
          <div className="sliderMagnitude">
            <input type="range" min="0" max="100" value="50" className="slider" id="magnitudeRange" onInput={(e) => updateValue(e.target)} />
            <span className="slider-value">50</span>
          </div>

        </div>
        <div className="Depth">
          <h4 className="Text">Depth</h4>
          <div className="sliderDepth">
            <input type="range" min="0" max="700" value="350" className="slider" id="depthRange" onInput={(e) => updateValue(e.target)} />
            <span className="slider-value">350</span>
          </div>
        </div>
      </div>
      <div className="Legend">
        <h4 className="Text">Legend</h4>
        <div className="LegendInfo">
          <p>
            <span className="MagnitudeClass">Micro (less than 2.0)</span> – Too small to be felt, detected only by seismographs.
            <br /><span className="MagnitudeClass">Minor (2.0–3.9)</span> – Weak tremors...
            {/* Continue the rest of your legend content */}
          </p>
        </div>

      </div>
    </div>
  );
};

export default InfoComponent;
