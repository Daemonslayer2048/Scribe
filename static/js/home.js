function DisableDevice(url, device){
  fetch(url + 'device/disable/' + device, {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(function ReloadPage(){
    location.reload(true)
  });
}

function EnableDevice(url, device){
  response = fetch(url + 'device/enable/' + device, {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(function ReloadPage(){
    location.reload(true)
  });
}
