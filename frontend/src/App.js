import React, { Component, useState } from 'react';
import { Key } from './key' // 引入 API key
import GoogleMapReact from 'google-map-react';
// 53.347816
// -6.259317
const MyPositionMarker = ({ text }) => <div>{text}</div>;

// Map
const SimpleMap = (props) => {
  const [myPosition, setMyPosition] = useState({
    lat: 53.347816,
    lng: -6.259317
  })

  const [mapApiLoaded, setMapApiLoaded] = useState(false)
  const [mapInstance, setMapInstance] = useState(null)
  const [mapApi, setMapApi] = useState(null)

  const apiHasLoaded = (map, maps) => {
    setMapInstance(map)
    setMapApi(maps)
    setMapApiLoaded(true)
  };

  const handleCenterChange = () => {
    if(mapApiLoaded) {
      setMyPosition({
        // center.lat()  center.lng() catch the center in the screen
        lat: mapInstance.center.lat(),
        lng: mapInstance.center.lng()
      })
    }
  }

  return (
    // Important! Always set the container height explicitly
    <div style={{ height: '100vh', width: '100%' }}>
      <GoogleMapReact
        bootstrapURLKeys={{ key: Key }}
        onBoundsChange={handleCenterChange}
        defaultCenter={props.center}
        defaultZoom={props.zoom}
        yesIWantToUseGoogleMapApiInternals // set true
        onGoogleApiLoaded={({ map, maps }) => apiHasLoaded(map, maps)} // execute after loading
      >
        <MyPositionMarker
          lat={myPosition.lat}
          lng={myPosition.lng}
          text="My Position"
        />
      </GoogleMapReact>
    </div>
  );
}

// Set defaultProps
SimpleMap.defaultProps = {
  center: {
    lat: 53.348358, 
    lng: -6.260327
  },
  zoom: 17
};


// App
function App() {
  return (
    <div className="App">
      <SimpleMap />
    </div>
  );
}

export default App;