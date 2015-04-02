var app = angular.module("ballotapi", [
    "leaflet-directive"
]);

app.controller('MainController', ['$scope', function($scope) {

    // make map
    angular.extend($scope, {
        san_fran: {
            lat: 37.78,
            lng: -122.42,
            zoom: 13
        },
        events: {},
        layers: {
            baselayers: {
                osm: {
                    name: 'OpenStreetMap',
                    url: 'https://{s}.tiles.mapbox.com/v3/examples.map-i875mjb7/{z}/{x}/{y}.png',
                    type: 'xyz'
                }
            }
        },
        defaults: {
            scrollWheelZoom: false
        }
    });

    // add marker
    $scope.markers = new Array();
    $scope.$on("leafletDirectiveMap.click", function(event, args){
        var leafEvent = args.leafletEvent;

        // only allow one marker
        $scope.markers[0] = {
            lat: leafEvent.latlng.lat,
            lng: leafEvent.latlng.lng,
            draggable: true
        };
    });

    // handle 'Find My Ballot'
    $scope.findBallot = function(){

        if(!$scope.markers[0]){
            alert('Please click on the map first!');
            return;
        }

        // animations (not angulartastic)
        // https://thinkster.io/egghead/animating-the-angular-way
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

        // update center (not working)
        $scope.san_fran = {
            lat: $scope.markers[0].lat,
            lng: $scope.markers[0].lng,
            zoom: 15
        };

        // should update scope with values
        $("#step1 span.step-header").text("Location:");
        $("#step1 span.step-value").text("37.7942635, -122.3955861");
    }
}]);