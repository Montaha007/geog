var map = L.map('map').setView([36.8, 10.2], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var LeafIcon = L.Icon.extend({
    options: {
        iconSize:     [32, 32],        // Square size for camera icon
        shadowSize:   [32, 32],        // Match icon size
        iconAnchor:   [16, 16],        // Center the icon
        shadowAnchor: [16, 16],        // Center the shadow
        popupAnchor:  [0, -16],        // Popup appears above icon
        shadowUrl:    ''
    }
});
var greenIcon = new LeafIcon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/5695/5695715.png',
});

var drawControl = new L.Control.Draw({
    position: 'topright',
    draw: {
        polygon: {
            allowIntersection: false,
            showArea: true,
            drawError: {
                color: 'orange',
                timeout: 1000
            },
            shapeOptions: {
                color: 'purple'
            }
        },
        polyline: {
            shapeOptions: {
                color: 'red'
            }
        },
        rectangle: {
            shapeOptions: {
                color: 'green'
            }
        },
        circle: {
            shapeOptions: {
                color: 'steelblue'
            }
        },
        marker: {
            icon: greenIcon
        }
    },
    edit: {
        featureGroup: drawnItems
    }
});

map.addControl(drawControl);

// Intercept draw:created to show Leaflet popup and save
map.on('draw:created', function (e) {
    var layer = e.layer;
    drawnItems.addLayer(layer); // Add immediately

    // Get center for polygons, or latlng for marker
    var latlng;
    if (layer.getLatLng) {
        latlng = layer.getLatLng();
    } else if (layer.getBounds) {
        latlng = layer.getBounds().getCenter();
    } else {
        latlng = map.getCenter();
    }

    // Create popup content
    var popupContent = `
        <div style="min-width:200px">
            <input type='text' id='popup-shape-name' class='form-control mb-2' placeholder='Enter shape name'>
            <input type='text' id='popup-rtsp-link' class='form-control mb-2' placeholder='Enter RTSP link'>
            <input type='text' id='popup-stream-id' class='form-control mb-2' placeholder='Enter Stream ID'>
            <button id='popup-save-btn' class='btn btn-success btn-sm w-100'>Save</button>
        </div>
    `;
    layer.bindPopup(popupContent).openPopup(latlng);

    // Wait for popup to render, then add event
    setTimeout(function() {
        document.getElementById('popup-save-btn').onclick = function() {
            var name = document.getElementById('popup-shape-name').value || 'Unnamed';
            var rtsp = document.getElementById('popup-rtsp-link').value || '';
            var streamId = document.getElementById('popup-stream-id').value || '';
            var geojson = drawnItems.toGeoJSON();
            geojson.name = name;
            geojson.rtsp = rtsp;
            geojson.stream_id = streamId;
            fetch('/geo/save/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(geojson)
            })
            .then(response => response.json())
            .then(result => {
                alert(result.message);
                layer.closePopup();
            })
            .catch(error => {
                console.error(error);
                alert("Failed to save.");
            });
        };
    }, 100);
});

// Helper to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let activeLayers = [];
// Visualize selected locations from the toggles in the dropdown

document.getElementById("visualizeSelectedBtn").addEventListener("click", () => {
    clearMap();

    // Only select checked checkboxes inside the dropdown menu
    const selectedIds = Array.from(document.querySelectorAll("#userLocationsList input[type=checkbox]:checked"))
        .map(checkbox => checkbox.value);

    selectedIds.forEach(id => {
        const location = locationData[id];
        if (!location) return;

        let layer;

        if (location.point) {
            // Point: [lat, lng]
            layer = L.marker(location.point).bindPopup(location.name);
        } else if (location.shape) {
            let latlngs;

            // Check if shape is nested: [[[lng, lat], [lng, lat], ...]]
            if (Array.isArray(location.shape[0][0])) {
                // Multi-ring Polygon: use only outer ring (first one)
                const outerRing = location.shape[0];
                latlngs = outerRing.map(coord => [coord[1], coord[0]]);
            } else {
                // Simple polygon
                latlngs = location.shape.map(coord => [coord[1], coord[0]]);
            }

            layer = L.polygon(latlngs, { color: 'blue' }).bindPopup(location.name);
        }

        if (layer) {
            layer.addTo(map);
            activeLayers.push(layer);
        }
    });

    // Show Clear Map button if anything was added
    if (activeLayers.length) {
        let group = L.featureGroup(activeLayers);
        map.fitBounds(group.getBounds(), { padding: [20, 20] }); // Optional: add padding
        document.getElementById("clearMapBtn").style.display = "inline-block";
    }
});

document.getElementById("clearMapBtn").addEventListener("click", () => {
    clearMap();
    document.getElementById("clearMapBtn").style.display = "none";
    document.querySelectorAll("#userLocationsList input[type=checkbox]:checked").forEach(cb => cb.checked = false);
});

function clearMap() {
    activeLayers.forEach(layer => map.removeLayer(layer));
    activeLayers = [];
}