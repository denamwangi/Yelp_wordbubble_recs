

var map;

    // var centerMapinit = new google.maps.LatLng(40.64317, -79.4066254);
function initMap(centerMap={lat: 43.64317, lng: -79.4066254}, zoom=10) {
        console.log('init map has been called ');
        var directionsService = new google.maps.DirectionsService;
        var directionsDisplay = new google.maps.DirectionsRenderer;
        // debugger;
          
        map = new google.maps.Map(document.getElementById('map'), {
          center: centerMap,
          zoom: zoom,
        });

        // addMarker();

}
        


// Helper functions for creating the map above. They take in data from teh json and pull whats needed to add data to the map

    function addMarker(businesses){
      // Adds the markers for each restaurant and adds an info window to each. First pulls the lat, longs and other info from the json then formats it for 
      // google maps, and  creates an info window
            
         // 1) Pull the data and iterate over each business' json
            for (var business in businesses) { 
                latitude = businesses[business]['latitude']
                longitude = businesses[business]['longitude']
                var markerInfo = businesses[business]['name']+ ' ('+businesses[business]['stars']+')'
                var location = {lat: latitude, lng: longitude};


          // 2)  Create the actual marker
                newMarker= formatMarker(location);

          // Add the info window on each marker
                addInfoWindow(newMarker, markerInfo )


        }
    }


    function formatMarker(myLatLng) {
      // Creates the actual google maps object that will be added to the map
      var marker = new google.maps.Marker({
              position: myLatLng,
              map: map,
            });
      
        return marker;
      }

    function addInfoWindow(marker, markerInfo) {
    //Creates an info window that will display the name of the restaurant (or number?)

        var contentString = '<div id="content">' +
          '<p>'+markerInfo+'</p>' +
          '</div>';

        var infoWindow = new google.maps.InfoWindow({
          content: contentString,
          maxWidth: 100
        });

        marker.addListener('mouseover', function() {
          infoWindow.open(map, marker);
        });
        marker.addListener('mouseout', function() {
          infoWindow.close(map, marker);
        });
    }