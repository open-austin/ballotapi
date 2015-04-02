var map = L.map('map').setView([37.78,-122.42],13);

L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
    maxZoom: 18,
    id: 'examples.map-i875mjb7'
}).addTo(map);

var marker;
map.on('click', function(e) {
    marker = new L.marker(e.latlng,{draggable: true});
    map.addLayer(marker);
});


var BALLOT_API = "http://50.116.6.242/(elections|measures|precincts)/";
$("#find-ballot").click(function(){
    $("#step2").hide();
    $("#map-wrapper").animate({"max-width": "300px"}, {
        "duration": 500,
        "queue": false,
    });
    $("#map").animate({"height": "200px"}, {
        "duration": 500,
        "queue": false,
        "complete": function(){
            $("#measures").show();
            $(".map-details").show();
        },
    });
    $("#step1 span.step-header").text("Location:");
    $("#step1 span.step-value").text("37.7942635, -122.3955861");
});

$("#change-location").click(function(e){
    e.preventDefault();
    $("#measures").hide();
    $(".map-details").hide();
    $("#map-wrapper").animate({"max-width": "100%"}, {
        "duration": 500,
        "queue": false,
    });
    $("#map").animate({"height": "450px"}, {
        "duration": 500,
        "queue": false,
        "complete": function(){
            $("#step2").show();
        },
    });
    $("#step1 span.step-header").text("Step 1:");
    $("#step1 span.step-value").text("Drop the pin on your home.");
});