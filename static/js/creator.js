console.log('creator.js script') 


fetch(`/metrics.json/${document.getElementById('username').value}` ) 
.then((response) => response.json())
.then((data) => {
  console.log(data.data);
  let videoCountData = [];
  let followersData = [];
  let dateData = []; 

  for (let datum of data.data) {
    videoCountData.push(datum.videos);
    followersData.push(datum.followers);
    dateData.push(datum.date); 
  }

  const mixedChart = new Chart(
    document.getElementById('historical-chart'), {
    data: {
        datasets: [{
            type: 'line',
            label: 'Video Count Dataset',
            data: videoCountData, 
            backgroundColor: [ 'rgb(176, 196, 177, 0.2)' ], 
            borderColor: [ 'rgb(74, 87, 89) '], 
        }, {
            type: 'bar',
            label: 'Follower Dataset',
            // data: [data.data.followers], 
            data: followersData,
            backgroundColor: [ 'rgb(176, 196, 177, 0.2)' ], 
            borderColor: [ 'rgb(74, 87, 89) '], 

        }],
        labels: dateData, 
    },
    options: {
      plugins: {
        legend: { 
          labels: { 
            font: { 
              family: "'Lato', sans-serif"
            }
          }
        }
      }, 
      responsive: true,
      maintainAspectRatio: false,  
      scales: {
        x: {
          display: true,
        },
        y: {
          display: true,
          type: 'logarithmic',
        }
      }

    },
  })});






const submitBtn = document.querySelector('form');

submitBtn.addEventListener('submit', (evt) => {
  evt.preventDefault();

  const queryString = new URLSearchParams({"username": document.getElementById('username').value }).toString();
  // you could also hard code url to '/status?order=123'
  const url = `/update?${queryString}`;


  fetch(url) 
  .then((response) => response.json())
  .then((data) => {
    console.log(data);{
    // document.getElementById('#update').innerText = data.followers;
    

    const testChart = new Chart(
      document.getElementById('current-chart'),
      {
        type: 'bar',
        label: 'Current metrics overview', 
        data: {
          labels: ['Followers', 'Following', 'Videos', 'Likes'],
          datasets: [
            {data: [ data.followers, data.following, data.videos, data.likes ], 
              backgroundColor: [ 'rgb(176, 196, 177, 0.2)' ], 
              borderColor: [ 'rgb(74, 87, 89) '], 
            }
          ],
        }, 
        options: {
          responsive: true,
          maintainAspectRatio: false,  
          scales: {
            x: {
              display: true,
            },
            y: {
              display: true,
              type: 'logarithmic',
            }
          },
          plugins: {
            legend: {
              display: false, 
              labels: {
                font: { 
                  family: "'Lato', sans-serif"
                }
              }
            }
          },
        },
      }
    );
    
  }})}); 


// // When the user scrolls the page, execute myFunction
// window.onscroll = function() {myFunction()};

// // Get the navbar
// var navbar = document.getElementById("navbar");

// // Get the offset position of the navbar
// var sticky = navbar.offsetTop;

// // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
// function myFunction() {
//   if (window.pageYOffset >= sticky) {
//     navbar.classList.add("sticky")
//   } else {
//     navbar.classList.remove("sticky");
//   }
// }
