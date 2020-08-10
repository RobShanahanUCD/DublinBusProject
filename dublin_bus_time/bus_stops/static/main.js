window.map = undefined;
// Location of Dublin
var dublin = {
  lat: 53.3498,
  lng: -6.2603,
};
var infoWindow = null;
var cityID = 7778677;

// Centre map on Dublin
function centerDublin(controlDiv, map) {
  // Set CSS for the control border.
  var controlUI = document.createElement("div");
  controlUI.style.backgroundColor = "#fff";
  controlUI.style.border = "2px solid #fff";
  controlUI.style.borderRadius = "2px";
  controlUI.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
  controlUI.style.cursor = "pointer";
  controlUI.style.height = "40px";
  controlUI.style.width = "40px";
  controlUI.style.marginTop = "10px";
  controlUI.style.marginLeft = "10px";
  controlUI.style.alignContent = "space-around";
  controlUI.title = "Center the map on Dublin";
  controlDiv.appendChild(controlUI);

  // Set CSS for the control interior.
  var controlImg = document.createElement("img");
  controlImg.src = "static/icons/centre.png";
  controlImg.setAttribute("height", "35");
  controlImg.setAttribute("width", "35");
  controlUI.appendChild(controlImg);

  // Event listener on button to recenter the map on Dublin
  controlUI.addEventListener("click", function () {
    map.setCenter(dublin);
    map.setZoom(14);
  });
}

function centerUser(controlDiv, map) {
  // Set CSS for the control border.
  var controlUI = document.createElement("div");
  controlUI.style.backgroundColor = "#fff";
  controlUI.style.border = "2px solid #fff";
  controlUI.style.borderRadius = "2px";
  controlUI.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
  controlUI.style.cursor = "pointer";
  controlUI.style.height = "40px";
  controlUI.style.width = "40px";
  controlUI.style.marginLeft = "10px";
  controlUI.style.alignContent = "space-around";
  controlUI.title = "Center the map on your location";
  controlDiv.appendChild(controlUI);

  // Set CSS for the control interior.
  var controlImg = document.createElement("img");
  controlImg.src = "static/icons/user.png";
  controlImg.setAttribute("height", "35");
  controlImg.setAttribute("width", "35");
  controlUI.appendChild(controlImg);

  // Event listener on button to recenter the map on the user's device location
  controlUI.addEventListener("click", function () {
    if (navigator.geolocation) {
      var userLocation;
      navigator.geolocation.getCurrentPosition(
        function (position) {
          var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          userLocation = new google.maps.Marker({
            position: pos,
            map: map,
          });
          userLocation.setPosition(pos);
          map.setCenter(pos);
          map.setZoom(14);
        },
        function () {
          handleLocationError(true, userLocation, map.getCenter());
        }
      );
    } else {
      // Browser doesn't support geolocation
      handleLocationError(false, userLocation, map.getCenter());
    }

    // Unable to find user's device location - throw error message to user
    function handleLocationError(browserHasGeolocation, infoWindow, pos) {
      infoWindow.setPosition(pos);
      infoWindow.setContent(
        browserHasGeolocation
          ? "Error: The Geolocation service failed."
          : "Error: Your browser doesn't support Geolocation."
      );
      infoWindow.open(map);
    }
  });
}

// Travel-Time Infomation Box
function travelTimeInfo(controlDiv, map, travelTimeVal) {
  // Set CSS for the control border.
  var controlUI = document.createElement("div");
  controlUI.style.backgroundColor = "#fff";
  controlUI.style.border = "2px solid #fff";
  controlUI.style.borderRadius = "2px";
  controlUI.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
  controlUI.style.height = "25px";
  controlUI.style.width = "260px";
  controlUI.style.marginTop = "10px";
  controlUI.style.marginLeft = "10px";
  controlUI.style.alignContent = "space-around";
  controlUI.innerHTML =
    "<h6 style='text-align: center;'><b>Travel-Time: " +
    travelTimeVal +
    " minutes</b></h6>";
  controlDiv.appendChild(controlUI);
}

// Initialize and add the map
function initMap() {
  // Centre the map at Dublin
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: dublin,
    // Allows control of position of MAP/SATELLITE element
    mapTypeControl: false,
    // Allows control of position of Zoom element
    zoomControl: true,
    zoomControlOptions: {
      position: google.maps.ControlPosition.LEFT_BOTTOM,
    },
    // Allows control of position of street view element
    streetViewControl: false,
    // Allows control of position of fullscreen element
    fullscreenControl: false,
  });

  // Create button to recenter map on Dublin
  var centerControlDivDublin = document.createElement("div");
  var centerControlDublin = new centerDublin(centerControlDivDublin, map);

  centerControlDivDublin.index = 1;
  map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(
    centerControlDivDublin
  );

  // Create button to recenter map on user's device location
  var centerControlDivUser = document.createElement("div");
  var centerControlUser = new centerUser(centerControlDivUser, map);

  centerControlDivUser.index = 1;
  map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(
    centerControlDivUser
  );

  new AutocompleteDirectionsHandler(map);
}

/**
 * @constructor
 */
function AutocompleteDirectionsHandler(map) {
  this.map = map;
  this.originID = null;
  this.destinationID = null;
  this.travelMode = "TRANSIT";
  this.directionsService = new google.maps.DirectionsService();
  this.directionsRenderer = new google.maps.DirectionsRenderer();
  this.directionsRenderer.setMap(map);

  var originInput = document.getElementById("origin");
  originInput.style.backgroundColor = "#fff";
  originInput.style.border = "2px solid #fff";
  originInput.style.borderRadius = "2px";
  originInput.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
  originInput.style.cursor = "pointer";
  originInput.style.height = "20px";
  originInput.style.width = "125px";
  originInput.style.marginTop = "10px";
  originInput.style.marginLeft = "10px";
  originInput.style.alignContent = "space-around";

  var destinationInput = document.getElementById("destination");
  destinationInput.style.backgroundColor = "#fff";
  destinationInput.style.border = "2px solid #fff";
  destinationInput.style.borderRadius = "2px";
  destinationInput.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
  destinationInput.style.cursor = "pointer";
  destinationInput.style.height = "20px";
  destinationInput.style.width = "125px";
  destinationInput.style.marginTop = "10px";
  destinationInput.style.marginLeft = "10px";
  destinationInput.style.alignContent = "space-around";

  var originAutocomplete = new google.maps.places.Autocomplete(originInput);
  //Specify just the place data fields needed
  originAutocomplete.setFields(["place_id"]);

  var destinationAutocomplete = new google.maps.places.Autocomplete(
    destinationInput
  );
  //Specify just the place data fields needed
  destinationAutocomplete.setFields(["place_id"]);

  this.setupPlaceChangedListener(originAutocomplete, "ORIG");
  this.setupPlaceChangedListener(destinationAutocomplete, "DEST");

  this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(originInput);
  this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(
    destinationInput
  );
}

AutocompleteDirectionsHandler.prototype.setupPlaceChangedListener = function (
  autocomplete,
  mode
) {
  var me = this;
  autocomplete.bindTo("bounds", this.map);

  autocomplete.addListener("place_changed", function () {
    var place = autocomplete.getPlace();

    if (!place.place_id) {
      window.alert("Please select an option from the dropdown list.");
      return;
    }
    if (mode === "ORIG") {
      me.originID = place.place_id;
    } else {
      me.destinationID = place.place_id;
    }
    me.route();
  });
};

AutocompleteDirectionsHandler.prototype.route = function () {
  if (!this.originID || !this.destinationID) {
    return;
  }
  var me = this;

  this.directionsService.route(
    {
      origin: { placeId: this.originID },
      destination: { placeId: this.destinationID },
      travelMode: this.travelMode,
      transitOptions: {
        modes: ["BUS"],
      },
    },
    function (response, status) {
      if (status === "OK") {
        me.directionsRenderer.setDirections(response);
        var busData = [];
        var walkingData = [];

        var responseData = response.routes[0].legs[0].steps;
        for (let i = 0; i < responseData.length; i++) {
          if (responseData[i]["travel_mode"] === "TRANSIT") {
            var busStep = {
              distance: responseData[i]["distance"]["value"],
              route: responseData[i]["transit"]["line"]["short_name"],
              duration: responseData[i]["duration"]["value"],
              departure: {
                name: responseData[i]["transit"]["departure_stop"]["name"],
                location: [
                  responseData[i]["transit"]["departure_stop"][
                    "location"
                  ].lat(),
                  responseData[i]["transit"]["departure_stop"][
                    "location"
                  ].lng(),
                ],
                timestamp: responseData[i]["transit"]["arrival_time"][
                  "value"
                ].valueOf(),
              },
              arrival: {
                name: responseData[i]["transit"]["arrival_stop"]["name"],
                location: [
                  responseData[i]["transit"]["arrival_stop"]["location"].lat(),
                  responseData[i]["transit"]["arrival_stop"]["location"].lng(),
                ],
                timestamp: responseData[i]["transit"]["arrival_time"][
                  "value"
                ].valueOf(),
              },
            };
            busData.push(busStep);
          } else if (responseData[i]["travel_mode"] === "WALKING") {
            walkingData.push(responseData[i]["duration"]["value"]);
          }
        }
        console.log({ walking_data: walkingData, bus_data: busData });
        console.log(
          JSON.stringify({ walking_data: walkingData, bus_data: busData })
        );
        axios
          .post("http://localhost:8000/predict/", {
            walking_data: walkingData,
            bus_data: busData,
          })
          .then((res) => {
            var journeyTime = JSON.stringify(
              res.data.PredicedJourneyTime.PredicedJourneyTime
            );
            journeyTime = Math.round(journeyTime / 60);
            showTravelTime(journeyTime);
            // alert("Estimated Travel-Time: " + journeyTime + " minutes");
            // console.log(res.data);
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        window.alert("Directions request failed due to " + status);
      }
    }
  );
};

function showTravelTime(data) {
  // Create information box for travel time
  var travelTimeDiv = null;
  travelTimeDiv = document.createElement("div");
  var travelTime = travelTimeInfo(travelTimeDiv, map, data);
  // alert("Estimated Travel-Time: " + data + " minutes");

  travelTimeDiv.index = 1;
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(travelTimeDiv);
}

// // Toggle the menu
// function toggleMenu() {
//   var x = document.getElementById("accordionMenu");
//   if (x.style.display === "block") {
//     x.style.display = "none";
//   } else {
//     x.style.display = "block";
//   }
// }

// Pull weather data from OpenWeatherMap API and display information on page
function weatherBalloon(cityID) {
  fetch(
    "https://api.openweathermap.org/data/2.5/weather?id=" +
      cityID +
      "&appid=b14191b52752bb618f8a512e1f0752b2"
  )
    .then(function (resp) {
      return resp.json();
    }) // Convert data to json
    .then(function (data) {
      drawWeather(data);
    })
    .catch(function () {
      // catch any errors
    });
}

function drawWeather(d) {
  var celcius = Math.round(parseFloat(d.main.temp) - 273.15);
  var iconCode = d.weather[0].icon;
  var iconURL = "http://openweathermap.org/img/wn/" + iconCode + "@2x.png";
  $("#weatherIcon").attr("src", iconURL);
  // Capatilize the weather description
  var weather_description = d.weather[0].description;
  var formatted_description = all_Caps(weather_description);
  document.getElementById("description").innerHTML = formatted_description;
  document.getElementById("temp").innerHTML = celcius + "&deg;C";
}

// When page loads call on function to pull weather data from API and display on page
window.onload = function () {
  weatherBalloon(cityID);
};
