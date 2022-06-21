// Initialize and add the map
function initMap() {
    // The location of Uluru
    const uluru = { lat: -25.344, lng: 131.031 };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: uluru,
    });
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
      position: uluru,
      map: map,
    });
  }

  window.initMap = initMap;

let van = document.querySelector('#van')
let ham = document.querySelector('#ham')
let otw = document.querySelector('#otw')

van.style.display = "flex"
ham.style.display = "none"
otw.style.display = "none"

const display_van = () => {
  van.style.display = "flex"
  ham.style.display = "none"
  otw.style.display = "none"
}

const display_ham = () => {
  van.style.display = "none"
  ham.style.display = "flex"
  otw.style.display = "none"
}

const display_otw = () => {
  van.style.display = "none"
  ham.style.display = "none"
  otw.style.display = "flex"
}
window.display_van = display_van;
window.display_ham = display_ham;
window.display_otw = display_otw;