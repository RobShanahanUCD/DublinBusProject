/* eslint-disable no-undef */
/* global google */
import React, { Component } from "react";
import {
  withGoogleMap,
  withScriptjs,
  GoogleMap,
  DirectionsRenderer,
} from "react-google-maps";

const GOOGLE_API_KEY = process.env.REACT_APP_GOOGLE_API_KEY;
const google = window.google;

class Map extends Component {
  constructor(props) {
    super(props);

    this.state = {
      location: {
        lat: 53.3498,
        lng: -6.2603,
      },
      loading: true,
      zoom: 14,
      directions: null,
    };
  }

  componentDidMount(props) {
    // const directionsService = google.maps.DirectionsService();

    // const origin = { lat: 53.3498, lng: -6.2603 };
    // const destination = { lat: 53.3498, lng: -6.23 };

    // directionsService.route(
    //   {
    //     origin: origin,
    //     destination: destination,
    //     travelMode: google.maps.TravelMode.BUS,
    //   },
    //   (result, status) => {
    //     if (status === google.maps.DirectionsStatus.OK) {
    //       this.setState({
    //         directions: result,
    //       });
    //     } else {
    //       console.error(`Error fetching directions ${result}`);
    //     }
    //   }
    // );

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
    const { loading, location } = this.state;
    const { google } = this.props;

    if (loading) {
      return null;
    }

    const GoogleMapTest = withGoogleMap((props) => (
      <GoogleMap defaultCenter={location} defaultZoom={this.state.zoom}>
        <DirectionsRenderer directions={this.state.directions} />
      </GoogleMap>
    ));

    return (
      <div style={{ marginTop: "56px" }}>
        <GoogleMapTest
          containerElement={<div style={{ height: `92vh`, width: "100%" }} />}
          mapElement={<div style={{ height: `100%` }} />}
        />
      </div>
    );
  }
}

export default Map;
