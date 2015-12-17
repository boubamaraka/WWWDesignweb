
// Global Maps Variables
var activities = ["Hiking", "Kayaking", "Swimming", "Skiing"]
var activeActivities = [];

var rootLatLng = {lat: 60.187, lng: 24.820};
var locations = [
    {coord: {lat: 60.220, lng: 24.865}, activityList: [0, 1, 0, 0], desc: "Strömbergin puisto", active: false, 
    photoCoord: {maxLat: 60.2214, minLat: 60.2185, maxLng: 24.8676, minLng: 24.8637}},
    {coord: {lat: 60.258, lng: 24.603}, activityList: [0, 0, 1, 0], desc: "Sorlammen luontopolku", active: false},
    {coord: {lat: 60.294, lng: 24.558}, activityList: [0, 1, 1, 1], desc: "Päivättärenpolku", active: false},
    {coord: {lat: 60.242, lng: 24.656}, activityList: [1, 0, 0, 0], desc: "Oittaan luontopolku", active: false},
    {coord: {lat: 60.188, lng: 24.813}, activityList: [0, 1, 0, 1], desc: "Laajalahden luontopolku", active: false,
    photoCoord: {maxLat: 60.2003, minLat: 60.1877, maxLng: 24.8217, minLng: 24.8122}},
    ];
var activeLocations = []
var map;
var markers = [];
var summerFilter = false;
var winterFilter = false;

// Global Places Variables
var service;

function initMap() {
  console.log("initMap");
  // Create a map object and specify the DOM element for display.
  map = new google.maps.Map(document.getElementById('gMap'), {
    center: rootLatLng,
    scrollwheel: true,
    zoom: 10
  });
  service = new google.maps.places.PlacesService(map);


  // Create a marker and set its position.
  for (var i = 0; i < locations.length; i++) {
    var title = "location: " + i;

    var marker = new google.maps.Marker({
      map: null,
      position: locations[i].coord,
      title: title
    });
    markers.push(marker);
    var dist = calculateDistance(locations[0], locations[i]);

    var infowindow = new google.maps.InfoWindow();
    var content = locations[i].desc + ", summer: " + locations[i].summer + ", winter: " + locations[i].winter;

    google.maps.event.addListener(marker,'click', (function(marker,content,infowindow){ 
        return function() {
            infowindow.setContent(content);
            infowindow.open(map,marker);
        };
    })(marker,content,infowindow));

  };  
}

function initActivities() {
  console.log("initActivities");

  for (var i = 0; i < activities.length; i++) {
    var activity = activities[i];
    activeActivities.push({name: activity, active: false});
  }
}

function getPlacePhotos(location) {
  lat = location.coord.lat;
  lng = location.coord.lng;
  console.log("getPlacePhotos");
  if (location.photoCoord != undefined) {
    maxLat = location.photoCoord.maxLat;
    maxLng = location.photoCoord.maxLng;
    minLat = location.photoCoord.minLat;
    minLng = location.photoCoord.minLng;
    var url_str = "http://www.panoramio.com/map/get_panoramas.php?set=public&from=0&to=10&minx=" + (minLng) + "&miny=" + (minLat) + "&maxx=" + (maxLng) + "&maxy=" + (maxLat) + "&size=medium&mapfilter=true";
  }
  else {
    var wiggle = 0.002;
    var url_str = "http://www.panoramio.com/map/get_panoramas.php?set=public&from=0&to=10&minx=" + (lng - wiggle) + "&miny=" + (lat - wiggle) + "&maxx=" + (lng + wiggle) + "&maxy=" + (lat + wiggle) + "&size=medium&mapfilter=true";
  }
  var desc = location.desc;
  console.log(url_str);
  var coord = new google.maps.LatLng(lat,lng);
  $.ajax({ 
   type: "GET",
   dataType: "jsonp",
   url: url_str,
   success: function(data){
      displayPhotos(data, desc);
   }
  });
}

function displayPhotos(data, desc) {
  //alert(JSON.stringify(data));
  //console.log(JSON.stringify(data));
  //console.log(JSON.stringify(data.photos));
  console.log(data.photos.length);
  var el = $("#locationPhotos");
  el.html("");
  el.append("<p>These photos have been taken near " + desc + "</p>");
  for (var i = 0; i < data.photos.length; i++) {
    var photo = data.photos[i]
    console.log(JSON.stringify(photo));
    el.append('<div class="col-md-2 col-sm-4 col-xs-6">');
    el.append('<a href="' + photo.photo_url + '"><img class="img-responsive customer-img" src="' + photo.photo_file_url + '" alt=""></a>');
    el.append('<p>author:' + photo.owner_name + '</p>');
    el.append('</div>');
    // TODO: PANORAMIO REQUIREMENTS
  }
  el.append("<img class='img-responsive customer-img' src='/static/media/Logo-panoramio-google.png' alt=''></img>");
  el.append("<p>Photos are collected automatically from <a href='http://www.panoramio.com/'>Panoramio</a><br>Photos provided by Panoramio are under the copyright of their owners<br>Clicking a photo will redirect you to the Panoramio service</p>");
}


function initFilters() {
  console.log("initFilters");

  var filterElement = $("#locationFilter");

  // Create Checkboxes in to locationForm
  var locationForm = $("#locationForm");
  for (var i = 0; i < activities.length; i++) {
    var activity = activities[i];
    locationForm.append("<input id='" + activity + "Chx' type='checkbox' name='activity' value='" + activity + "'><label class='checkbox inline' for='" + activity + "Chx'>&nbsp;" + activity + "</label><br>");
  }

  $("#markerList").click(function(event) {
    console.log("markerList click");
    var target = $(event.target);
    var index = target.index();
    locLat = activeLocations[index].coord.lat;
    locLng = activeLocations[index].coord.lng;
    var locCoord = new google.maps.LatLng(locLat, locLng);
    map.panTo(locCoord);
    map.setZoom(11);
    getPlacePhotos(activeLocations[index]);
  });

  // Create Listeners for activities
  console.log("Create Listeners");

  function generateActivityListener(j, selectorStr) {
    return function(event) {
      activeActivities[j].active = $(selectorStr).prop("checked");
      updateMarkers();
      //getPlacePhotos(locations[j]);
    };
  }

  for (var i = 0; i < activities.length; i++) {
    var activity = activities[i];
    var selectorStr = "#" + activity + "Chx";
    $(selectorStr).click(generateActivityListener(i, selectorStr));
  }
}

// Sets the map on all markers in the array.
function setMapOnAll(map, locations) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers(locations) {
  setMapOnAll(null, locations);
}

// Shows any markers currently in the array.
function showMarkers(locations) {
  setMapOnAll(map, locations);
}


function updateMarkers() {

  for (var i = 0; i < markers.length; i++) {
    var marker = markers[i];
    var location = locations[i];
    location.active = false;
    marker.setMap(null);
    for (var j = 0; j < activities.length; j++) {
      var activity = activities[j];
      if (activeActivities[j].active && location.activityList[j] == 1) {
        location.active = true;
        marker.setMap(map);
      }
    }
  }
  updateLocationList();

}

function updateLocationList() {
  activeLocations = []
  var markerList = $("#markerList");
  markerList.html("");
  var idx = 0
  for (var i = 0; i < locations.length; i++) {
    var location = locations[i];
    if (location.active === true) {
      activeLocations[idx] = location;
      markerList.append("<li id='locationElement" + i + "'>" + location.desc + "</li>");
      idx += 1;
    }
  }
}

function calculateDistance(coord1, coord2) {
  var R = 6371; // Radius of the earth in km
  var dLat = (coord1.coord.lat-coord2.coord.lat).toRad();  // Javascript functions in radians
  var dLon = (coord1.coord.lng-coord2.coord.lng).toRad(); 
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
          Math.cos(coord1.coord.lat.toRad()) * Math.cos(coord2.coord.lat.toRad()) * 
          Math.sin(dLon/2) * Math.sin(dLon/2); 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c;
  return d;

}

if (typeof(Number.prototype.toRad) === "undefined") {
  Number.prototype.toRad = function() {
    return this * Math.PI / 180;
  }
}

//initMap();
initActivities();
initFilters();