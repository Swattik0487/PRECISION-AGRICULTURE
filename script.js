document.addEventListener("DOMContentLoaded", function () {
    // Initialize the map
    var map = L.map('map-container').setView([8.0844, 77.5495 ], 20); // Centered on Kanyakumari

    // Load OSM Tile Layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Taluks GeoJSON (Add more as needed)
    var taluks = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": { "name": "Agastheeswaram" },
                "geometry": {
                    "type": "Point",
                    "coordinates": [77.5453, 8.1018]
                }
            },
            {
                "type": "Feature",
                "properties": { "name": "Thovalai" },
                "geometry": {
                    "type": "Point",
                    "coordinates": [77.4100, 8.2937]
                }
            },
            {
                "type": "Feature",
                "properties": { "name": "Kalkulam" },
                "geometry": {
                    "type": "Point",
                    "coordinates": [77.3205, 8.2325]
                }
            }
        ]
    };

    // Add Taluk Markers
    L.geoJSON(taluks, {
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng).bindPopup(feature.properties.name);
        },
        onEachFeature: function (feature, layer) {
            layer.on('click', function () {
                document.getElementById("selected-taluk").innerText = feature.properties.name;
            });
        }
    }).addTo(map);

    map.on('click', function (e) {
        var lat = e.latlng.lat.toFixed(4);
        var lng = e.latlng.lng.toFixed(4);
        alert("Selected Coordinates: " + lat + ", " + lng);
    });
});

// Function to switch tabs
function showTab(tabName) {
    let tabs = document.querySelectorAll(".tab-content");
    tabs.forEach(tab => tab.classList.remove("active"));

    let buttons = document.querySelectorAll(".tab-button");
    buttons.forEach(button => button.classList.remove("active"));

    document.getElementById(tabName).classList.add("active");
    document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add("active");
}
