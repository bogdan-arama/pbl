import React from 'react';
import './App.css';
import InteractiveMap from './components/InteractiveMap';
import InfoComponent from './components/InfoComponent';

function App() {
  return (
    <div className="App">
      <InteractiveMap />
      <InfoComponent />
    </div>
  );
}

export default App;
