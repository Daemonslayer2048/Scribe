function DisableDevice(device){
  fetch('http://127.0.0.1:5000/device/disable/' + device, {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(function ReloadPage(){
    location.reload(true)
  });
}

function EnableDevice(device){
  response = fetch('http://127.0.0.1:5000/device/enable/' + device, {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(function ReloadPage(){
    location.reload(true)
  });
}
