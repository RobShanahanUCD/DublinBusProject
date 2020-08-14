//Weather function showing current weather from OpenWeatherMap API
const locationElement = document.querySelector(".location");
const iconElement = document.querySelector(".weatherIcon");
const temperatureElement = document.querySelector(".temperature p");
const descriptionElement = document.querySelector(".description p");

//Create the empty weather object
const weather = {};

//Define the temperature units
weather.temperature = {
  unit: "celcius"
}

//City ID for Dublin, IE and the OWM API key
const cityID = 7778677;
const weatherKey = "b14191b52752bb618f8a512e1f0752b2";

// Pull weather data from OpenWeatherMap API and display information on page
function getWeather() {
  let api = `https://api.openweathermap.org/data/2.5/weather?id=${cityID}&appid=${weatherKey}`;

  fetch(api)
    .then(function (response) {
      let data = response.json();
      return data;
    })
    .then(function (data) {
      weather.temperature.value = Math.floor(data.main.temp - 273);
      weather.description = data.weather[0].description;
      weather.iconId = data.weather[0].icon;
      weather.city = data.name;
      weather.country = data.sys.country;
    })
    .then(function () {
      showWeather();
    })
    .catch(function () {
      // catch any errors
    });
}

//Display the contents of the weather object on the screen
function showWeather() {
  locationElement.innerHTML = `${weather.city}, ${weather.country}`;
  iconElement.innerHTML = `<img src="static/icons/${weather.iconId}.png"/>`;
  temperatureElement.innerHTML = `${weather.temperature.value}°<span>C</span>`;
  descriptionElement.innerHTML = weather.description;
}

// When page loads call on function to pull weather data from API and display on page
window.onload = function () {
  getWeather();
};
