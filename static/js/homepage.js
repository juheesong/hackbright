const testChart = new Chart(
  document.getElementById('test-chart'),
  {
    type: 'bar',
    data: {
      labels: ['Followers', 'Following', 'Videos'],
      datasets: [
        {data: [ data.followers, data.following, data.videos ]}
      ]
    }
  }
);
});






function login() {
    fetch('/loginxxxx')
      .then((response) => response.text())
      .then((fortune) => {
        document.querySelector('#fortune-text').innerHTML = fortune;
      });
  }
  
  document.querySelector('#get-fortune-button').addEventListener('click', showFortune);
  
  // PART 2: SHOW WEATHER
  
  function showWeather(evt) {
    evt.preventDefault();
    const zipcode = document.querySelector('#zipcode-field').value;
    const url = `/weather?zipcode=${zipcode}`;
    fetch(url)
      .then((response) => response.json())
      .then((jsonData) => {
        document.querySelector('#weather-info').innerText = jsonData.forecast;
      });
  }
  
  document.querySelector('#weather-form').addEventListener('submit', showWeather);
  