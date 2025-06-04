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
document.getElementById('save-btn').onclick = function() {
    var data = drawnItems.toGeoJSON();
    var json = JSON.stringify(data, null, 2);
    var blob = new Blob([json], {type: "application/json"});
    var url  = URL.createObjectURL(blob);

    var a = document.createElement('a');
    a.download = "data.geojson";
    a.href = url;
    a.textContent = "Download GeoJSON";

    a.click();
    URL.revokeObjectURL(url);
};