function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: 49.1951, lng: 16.6068 },
  });

  const events = JSON.parse(document.getElementById("events-data").textContent);

  events.forEach((event) => {
    const marker = new google.maps.Marker({
      position: { lat: event.latitude, lng: event.longitude },
      map: map,
      title: event.name,
    });

    const infoWindow = new google.maps.InfoWindow({
      content: `
                <div>
                    <h5>${event.name}</h5>
                    <p>${event.description}</p>
                    <p><small>${event.date}</small></p>
                </div>
            `,
    });

    marker.addListener("click", function () {
      infoWindow.open(map, marker);
    });
  });
}
