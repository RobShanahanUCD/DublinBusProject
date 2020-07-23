/* eslint-disable no-undef */
/* global google */
import React, { Component } from "react";
import { compose, withProps } from "recompose";
import {
  withGoogleMap,
  withScriptjs,
  GoogleMap,
  DirectionsRenderer,
  Marker,
  InfoWindow,
} from "react-google-maps";

const GoogleMapTest = compose(
  withProps({
    googleMapURL:
      "https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places,directions",
    loadingElement: <div style={{ height: "100%" }} />,
    containerElement: <div style={{ height: `92vh`, width: "100%" }} />,
    mapElement: <div style={{ height: `100%` }} />,
  }),
  withScriptjs,
  withGoogleMap
)((props) => (
  <GoogleMap defaultCenter={this.state.location} defaultZoom={this.state.zoom}>
    {props.isMarkerShown && <Marker position={this.state.location} />}
    <DirectionsRenderer directions={this.state.directions} />
  </GoogleMap>
));

class Map extends Component {
  state = {
    isMarkerShown: false,
    zoom: 14,
    loading: true,
    directions: null,
    location: {
      lat: 53.3498,
      lng: -6.2603,
    },
  };

  componentDidMount() {
    // this.delayedShowMarker()

    const directionsService = new google.maps.DirectionsService();

    const origin = { lat: 53.3498, lng: -6.2603 };
    const destination = { lat: 53.3498, lng: -6.23 };

    directionsService.route(
      {
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.BUS,
      },
      (result, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          this.setState({
            directions: result,
          });
        } else {
          console.error(`Error fetching directions ${result}`);
        }
      }
    );

    navigator.geolocation.getCurrentPosition(
      (position) => {
        console.log("Geolocation successful", position);
        const { latitude, longitude } = position.coords;
        this.setState({
          location: {
            lat: latitude,
            lng: longitude,
          },
          loading: false,
        });
      },
      () => {
        this.setState({ loading: false });
      }
    );
  }

  render() {
    return (
      <div style={{ marginTop: "56px" }}>
        <GoogleMapTest isMarkerShown />
      </div>
    );
  }
}

export default Map;
