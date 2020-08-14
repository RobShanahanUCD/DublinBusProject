window.map = undefined;
// Location of Dublin
var dublin = {
  lat: 53.3498,
  lng: -6.2603,
};
var infoWindow = null;

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

  var travelTime = document.getElementById("travel");
  travelTime.style.backgroundColor = "#fff";
  travelTime.style.border = "2px solid #fff";
  travelTime.style.borderRadius = "2px";
  travelTime.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
  travelTime.style.height = "25px";
  travelTime.style.width = "260px";
  travelTime.style.textAlign = "center";
  travelTime.style.fontSize = "18px";
  travelTime.style.marginTop = "10px";
  travelTime.style.marginLeft = "10px";
  travelTime.style.alignContent = "space-around";
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(travelTime);

  var details = document.getElementById("details");
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(details);
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

//Function to check if there has been a change in the Directions input boxes.
//From: https://developers.google.com/maps/documentation/javascript/places-autocomplete
AutocompleteDirectionsHandler.prototype.setupPlaceChangedListener = function (
  autocomplete,
  mode
) {
  var me = this;
  autocomplete.bindTo("bounds", this.map);

  autocomplete.addListener("place_changed", function () {
    var place = autocomplete.getPlace();

    if (!place.place_id) {
      window.alert("Please enter a valid address.");
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

//Function to generate the route from the directions results
//From: https://developers.google.com/maps/documentation/javascript/places-autocomplete
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

        var dirInfo = response.routes[0].legs[0];
        var responseData = response.routes[0].legs[0].steps;
        writeDirections(dirInfo, responseData);
        console.log("Directions object:", response);
        console.log("Response Data:", responseData);
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

//Function showing estimated travel time calculated by ML model
function showTravelTime(data) {
  const estimate = document.querySelector("#travel");
  estimate.innerHTML = ("Travel-Time: " + data + " Minutes");


  document.getElementById("travel").style.display = "block";
  document.getElementById("details").style.display = "block";

  document.getElementById("directionsPanel").style.display = "none";
}

//Toggle button to show text directions
function showDirections() {
  var x = document.getElementById("directionsPanel");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
}

//Function to write the direction steps from the DirectionsRenderer result
function writeDirections(dir, steps) {
  var content = document.getElementById("detailedDirections");
  content.innerHTML = "";
  content.innerHTML += "<p><b>Total Distance: " + dir.distance.text + "</b></p>";
  content.innerHTML += "<h6><b>" + dir.start_address + "</b></h6>";

  for (var i = 0; i < steps.length; i++) {
    content.innerHTML += "<p><b>" + (i + 1) + ". </b>" + steps[i].instructions + "</p><small>" + steps[i].distance.text + "</small>";
  }

  content.innerHTML += "<h6><b>" + dir.end_address + "</b></h6>";
}