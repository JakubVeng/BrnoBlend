// Initialize the "load events" button
document
  .getElementById("loadEventsButton")
  .addEventListener("click", async () => {
    try {
      const response = await fetch("/update-events", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error("Failed to load new events");
      }
      alert("New events loaded successfully");
      // Optionally, refresh the page or update the UI as needed
    } catch (error) {
      console.error("Error loading new events:", error);
      alert("Failed to load new events");
    }
  });

let map;
let marker;
let resultsMap;
let markers = [];
let infoWindow = null; // Variable to store the currently open info window

// Function to initialize Google Maps
function initMaps() {
  // Initialize the main results map
  resultsMap = new google.maps.Map(document.getElementById("results-map"), {
    center: { lat: 0, lng: 0 }, // Default center if no events are loaded
    zoom: 2, // Adjust zoom level as needed
  });

  // Initialize the detail modal map
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 0, lng: 0 }, // Default center if no events are loaded
    zoom: 10, // Adjust zoom level as needed
  });

  // Add markers for all events on the results map
  const events = JSON.parse(eventsData);
  events.forEach((event) => {
    const eventCoords = {
      lat: parseFloat(event.latitude),
      lng: parseFloat(event.longitude),
    };
    const eventMarker = new google.maps.Marker({
      position: eventCoords,
      map: resultsMap,
      title: event.name,
    });

    eventMarker.addListener("click", () => {
      if (infoWindow) {
        infoWindow.close();
      }

      infoWindow = new google.maps.InfoWindow({
        content: eventMarker.title,
      });

      infoWindow.open(resultsMap, eventMarker);
    });

    // Store the marker
    markers.push(eventMarker);
  });

  // Adjust the center and zoom level of the results map to fit all markers
  if (markers.length > 0) {
    const bounds = new google.maps.LatLngBounds();
    markers.forEach((marker) => bounds.extend(marker.getPosition()));
    resultsMap.fitBounds(bounds);
  }
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
  const eventDetailsModal = new bootstrap.Modal(
    document.getElementById("eventDetailsModal"),
  );
  eventDetailsModal.show();
}
