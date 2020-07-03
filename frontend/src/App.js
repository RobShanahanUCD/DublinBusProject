import React, { Component, useState, useEffect, useRef} from 'react';
import { Button, ButtonGroup } from "reactstrap";
import { debounce } from 'lodash' //Autocomplete time delay setting
import { Key } from './key' // API key
import {API_URL_PREDICT} from './Api' //backend URL
import GoogleMapReact from 'google-map-react';
import axios from "axios";
import DatePicker from "react-datepicker";

// Default Dublin center
let cityCenter = {
    lat: 53.347816,
    lng: -6.259317
};


const MyPositionMarker = ({ text }) => <div>{text}</div>;

const Marker = ({ icon, text }) => (
  <div>
    <img style={{ height: '30px', width: '30px' }} alt="icon" src={icon} />
    <div>{text}</div>
  </div>
)


// Map
const SimpleMap = (props) => {
  const [myPosition, setMyPosition] = useState({
    lat: cityCenter.lat,
    lng: cityCenter.lng
  })

  // Default state
  let inputRef = useRef(null);
  let inputRefTo = useRef(null);

  const [startDate, setStartDate] = useState(new Date());
  
  const [mapApiLoaded, setMapApiLoaded] = useState(false)
  const [mapInstance, setMapInstance] = useState(null)
  const [mapApi, setMapApi] = useState(null)
  
  const apiHasLoaded = (map, maps) => {
    setMapInstance(map)
    setMapApi(maps)
    setMapApiLoaded(true)
  };

  const [searchType, setSearchType] = useState(['transit_station'])

  const SearchType = ({ text, type }) => {
    return <input type="button" value={text} name={type} />
  }
  
  // Find bus stop
  const [places, setPlaces] = useState([])

  const findLocation = () => {
    if(mapApiLoaded) {
      const service = new mapApi.places.PlacesService(mapInstance)

      const request = {
        location: myPosition,
        radius: 1000,
        type: searchType
      };

      service.nearbySearch(request, (results, status) => {
        if(status === mapApi.places.PlacesServiceStatus.OK) {
          setPlaces(results)
        }
      })
    }
  }

  useEffect(() => {
    findLocation()
  }, [searchType, myPosition, mapApiLoaded])

  const handleCenterChange = ({bound, zoom, center}) => {
    if(mapApiLoaded) {
      setMyPosition({
        // center.lat()  center.lng() catch the center in the screen
        lat: mapInstance.center.lat(),
        lng: mapInstance.center.lng()
      })
    }
  }

  const [inputText, setInputText] = useState('')

  const handleInput = () =>{
    setInputText(inputRef.current.value)
  }

  const handleInputTo = () =>{
    setInputText(inputRefTo.current.value)
  }

  const handleSearchType = e => {
    setSearchType(e.target.name)
  }
  
  // Change map type
  const [mapType, setMapType] = useState('roadmap')

  const handleMapTypeId = e => {
    setMapType(e.target.name)
  }

  const [autocompleteResults, setAutocompleteResults] = useState([])
  
  const handleAutocomplete = () =>{
    if (mapApiLoaded) {
      const serviceFrom = new mapApi.places.AutocompleteService()
      const serviceTo = new mapApi.places.AutocompleteService()
      const request ={
        input: inputText
      }

      serviceFrom.getPlacePredictions(request, (results, status, ) => {
        if(status === mapApi.places.PlacesServiceStatus.OK){
          setAutocompleteResults(results)
        }
      });

      serviceTo.getPlacePredictions(request, (results, status, ) => {
        if(status === mapApi.places.PlacesServiceStatus.OK){
          setAutocompleteResults(results)
        }
      });

    }
  }
  useEffect(()=>{
    handleAutocomplete()
  }, [inputText])

  const [currentCenter, setCurrentCenter] = useState({
    lat: cityCenter.lat,
    lng: cityCenter.lng
  })

  const handleClickToChangeMyPosition = e => {
    const placeId = e.target.getAttribute('dataid')
    const service = new mapApi.places.PlacesService(mapInstance)
    const request = {
      placeId: placeId,
      fields: [
        'geometry'
      ]
    }
    service.getDetails(request, (result, status)=>{
      if( status === mapApi.places.PlacesServiceStatus.OK) {
        const newPosition = {
          lat: result.geometry.location.lat(),
          lng: result.geometry.location.lng()
        }
        setCurrentCenter(newPosition) // change view
        setMyPosition(newPosition) // change MyPosition
        setAutocompleteResults([]) // Empty search list
        inputRef.current.value = '' // Empty <input>
      }
    })
  }

  const handleSubmit = e => {
    e.preventDefault();
    axios({
      method: 'post',
      url: API_URL_PREDICT, 
      data: {
      "route": 1,
      "time" : 2
      }
    })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }


  return (
      <div style={{ height: '100vh', width: '100%' }}>
      
      <div>
        <div class="form">
        <Button onClick={handleSubmit}>Test</Button> 
        From: <input ref={inputRef} type="text" onChange={ debounce(handleInput, 500) } /><br/>
        To: <input ref={inputRefTo} type="text" onChange={ debounce(handleInputTo, 500) } /><br/> 
        Departure Date<DatePicker
          selected={startDate}
          onChange={date => setStartDate(date)}
          timeFormat="HH:mm"
          timeIntervals={15}
          timeCaption="time"
          dateFormat="MMMM d, yyyy h:mm aa"
          showTimeSelect
          popperPlacement="bottom-start"
          class="react-date-picker"
          popperModifiers={{
            flip: {
              enabled: false
            },
            preventOverflow: {
              enabled: true,
              escapeWithReference: false
            }
          }}

        />
        
        </div>
        <div onClick={handleClickToChangeMyPosition} class="search"> 
          {(autocompleteResults && inputText) &&
          autocompleteResults.map(item=>(
            <div key={item.id} dataid={item.place_id} id="search-list">
              {item.description}
            </div>
          ))}
        </div>
      </div>
      
      <div onClick={handleSearchType} class="search-place">
        <SearchType text="Bus Stop" type="transit_station" />
        <SearchType text="Tourist Spot" type="tourist_attraction" />
      </div>
      <div class="map-type">
        <input type="button" value="Satellite" onClick={ handleMapTypeId } name="hybrid" />
        <input type="button" value="Road" onClick={ handleMapTypeId } name="roadmap" />
      </div>
      <GoogleMapReact
        bootstrapURLKeys={{
          key: Key,
          libraries:['places'] // Our api
        }}
        //hacky way to fix bug
        distanceToMouse={()=>{}}

        center={currentCenter}
        options={{ mapTypeId: mapType }}
        onChange={handleCenterChange}
        defaultCenter={props.center}
        defaultZoom={props.zoom}
        yesIWantToUseGoogleMapApiInternals
        //map: map itself, maps: google map object 
        onGoogleApiLoaded={({ map, maps }) => apiHasLoaded(map, maps)}
        
      >
        <MyPositionMarker
          lat={myPosition.lat}
          lng={myPosition.lng}
        />
        {places.map(item=>(
          <Marker
            icon={item.icon}
            key={item.id}
            lat={item.geometry.location.lat()}
            lng={item.geometry.location.lng()}
            text={item.name}
            placeId={item.place_id}
          />
        ))}
      </GoogleMapReact>
    </div>
  );
}

// Set defaultProps
SimpleMap.defaultProps = {
  center: {
    lat: cityCenter.lat,
    lng: cityCenter.lng
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