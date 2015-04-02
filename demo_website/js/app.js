var app = angular.module("ballotapi", ["leaflet-directive"]);

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
}]);