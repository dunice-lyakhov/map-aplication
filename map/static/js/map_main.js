let map;
let geocoder;
let markers = [];

function initMap() {
  var uluru = {lat: -25.363, lng: 131.044};
  geocoder = new google.maps.Geocoder();

  map = new google.maps.Map($('#map-container')[0], {
    zoom: 4,
    center: uluru
  });
    
  // Listeners
  map.addListener('click', onMapClick);
}

function onMapClick($event) {
  if(!map) return;

  $.ajax({
    type: "POST",
    url: '/geodata-points/',
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      lat: $event['latLng'].lat(),
      lng: $event['latLng'].lng()
    },
    success: function(data) {
      if(data['status'] == 'success') {
        data = data['data'];

        markers.push(new google.maps.Marker({
            position: new google.maps.LatLng(data['lat'], data['lng']),
            map: map
        }));

        $('.list-address').append('' +
          '<div>' +
          '<span><strong>Address:</strong> ' + data['address'] + '</span>' +
          '<span><strong>Latitude:</strong> ' + data['lat'] + '</span>' +
          '<span><strong>Longitude:</strong> ' + data['lng'] + '</span>' +
          '</div>'
        )
      } else {
        // Create error handling on the client.
        console.log(data['message'])
      }
    }
  });
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = $.trim(cookies[i]);

      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function reset() {
  $.ajax({
    type: "DELETE",
    url: '/geodata-points/',
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    success: function(data) {
      location.reload();
    }
  });
}

$('.reset-button').on('click', reset);
