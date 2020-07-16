import React from "react";
import ReactDOM from "react-dom";

const mapStyles = {
  map: {
    position: "fixed",
    width: "100vw",
    height: "93vh",
    marginTop: "56px",
  },
};

// const camelize = function(str) {
//   return str.split(' ').map(function(word){
//     return word.charAt(0).toUpperCase() + word.slice(1);
//   }).join('');
// }

// const evtNames = ['ready', 'click', 'dragend'];

export class CurrentLocation extends React.Component {
  constructor(props) {
    super(props);

    const { lat, lng } = this.props.initialCenter;
    this.state = {
      currentLocation: {
        lat: lat,
        lng: lng,
      },
    };
  }

  componentDidUpdate(prevProps, prevState) {
    if (prevProps.google !== this.props.google) {
      this.loadMap();
    }
    if (prevState.currentLocation !== this.state.currentLocation) {
      this.recenterMap();
    }
  }

  recenterMap() {
    const map = this.map;
    const current = this.state.currentLocation;

    const google = this.props.google;
    const maps = google.maps;

    if (map) {
      let center = new maps.LatLng(current.lat, current.lng);
      map.panTo(center);
    }
  }

  componentDidMount() {
    if (this.props.centerAroundCurrentLocation) {
      if (navigator && navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((pos) => {
          const coords = pos.coords;
          this.setState({
            currentLocation: {
              lat: coords.latitude,
              lng: coords.longitude,
            },
          });
        });
      }
    }
    this.loadMap();
  }

  loadMap() {
    if (this.props && this.props.google) {
      //Checks if google is available
      const { google } = this.props;
      const maps = google.maps;

      const mapRef = this.refs.map;

      //Reference to the actual DOM element
      const node = ReactDOM.findDOMNode(mapRef);

      let { zoom } = this.props;
      const { lat, lng } = this.state.currentLocation;
      const center = new maps.LatLng(lat, lng);
      const mapConfig = Object.assign(
        {},
        {
          center: center,
          zoom: zoom,
        }
      );
      //maps.Map() is the constructor that instantiates the map
      this.map = new maps.Map(node, mapConfig);
      // evtNames.forEach((e) => {
      //   this.map.addListener(e, this.handleEvent(e));
      // });
    }
  }

  // handleEvent(evtName) {
  //   let timeout;
  //   const handlerName = `on${camelize(evtName)}`;;

  //   return (e) => {
  //     if (timeout) {
  //       clearTimeout(timeout);
  //       timeout = null;
  //     }
  //     timeout = setTimeout(() => {
  //       if (this.props[handlerName]) {
  //         this.props[handlerName](this.props, this.map, e);
  //       }
  //     }, 0);
  //   }
  // }

  renderChildren() {
    const { children } = this.props;

    if (!children) return;

    return React.Children.map(children, (c) => {
      if (!c) return;
      return React.cloneElement(c, {
        map: this.map,
        google: this.props.google,
        mapCenter: this.state.currentLocation,
      });
    });
  }

  render() {
    const style = Object.assign({}, mapStyles.map);
    return (
      <div>
        <div style={style} ref="map">
          Loading map...
        </div>
        {this.renderChildren()}
      </div>
    );
  }
}

export default CurrentLocation;

// CurrentLocation.propTypes = {
//   google: React.PropTypes.object,
//   zoom: React.PropTypes.number,
//   initialCenter: React.PropTypes.object,
//   centerAroundCurrentLocation: React.PropTypes.bool,
//   onMove: React.PropTypes.func,
//   evtNames: evtNames.forEach(e => Map.propTypes[camelize(e)] = T.func)
// }

CurrentLocation.defaultProps = {
  zoom: 14,
  initialCenter: {
    lat: 53.34,
    lng: -6.26,
  },
  // onMove: function() {}, // default prop
  // centerAroundCurrentLocation: false,
  // visible: true
};
