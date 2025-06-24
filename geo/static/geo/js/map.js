var map = L.map('map').setView([33.892166, 9.561555499999997], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var LeafIcon = L.Icon.extend({
    options: {
        iconSize:     [38, 95],
        shadowSize:   [50, 64],
        iconAnchor:   [22, 94],
        shadowAnchor: [4, 62],
        popupAnchor:  [-3, -76],
        shadowUrl:    'https://www.ippc.int/static/leaflet/images/leaf-shadow.png'
    }
});

var greenIcon = new LeafIcon({
    iconUrl: 'https://www.ippc.int/static/leaflet/images/leaf-green1.png'
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

map.on('draw:created', function (e) {
    var layer = e.layer;
    drawnItems.addLayer(layer);
});

// Save as GeoJSON button

document.getElementById('save-btn').onclick = function () {
    var name = document.getElementById('shape-name').value || 'Unnamed';
    var rtsp = document.getElementById('rtsp-link').value || '';
    var geojson = drawnItems.toGeoJSON();

    if (!geojson.features.length) {
        alert("Please draw a shape first.");
        return;
    }

    geojson.name = name;
    geojson.rtsp = rtsp;

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
    })
    .catch(error => {
        console.error(error);
        alert("Failed to save.");
    });
};

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



// ...existing code...

// ...existing code...