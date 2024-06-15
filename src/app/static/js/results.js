let map;
let marker;

// Function to initialize Google Map
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 0, lng: 0 }, // Default center if no events are loaded
    zoom: 10, // Adjust zoom level as needed
  });
}

// Function to show event details and map
function showEventDetails(name, text, categories, latitude, longitude) {
  // Set modal title and event details
  document.getElementById("eventDetailsModalLabel").innerText = name;
  const detailsList = document.getElementById("eventDetailsList");
  detailsList.innerHTML = `
    <li><strong>Text:</strong> ${text}</li>
    <li><strong>Categories:</strong> ${categories}</li>
  `;

  // Initialize map with event coordinates
  const eventCoords = { lat: parseFloat(latitude), lng: parseFloat(longitude) };
  map.setCenter(eventCoords); // Center map on event location
  map.setZoom(14); // Set zoom level for event

  // Remove previous marker if exists
  if (marker) {
    marker.setMap(null);
  }

  // Add marker for event location
  marker = new google.maps.Marker({
    position: eventCoords,
    map: map,
    title: name,
  });

  // Open the modal
  const eventDetailsModal = new bootstrap.Modal(document.getElementById("eventDetailsModal"));
  eventDetailsModal.show();
}
