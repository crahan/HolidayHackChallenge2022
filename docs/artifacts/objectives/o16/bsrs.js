var queryString;
var guid;
var in_trans = false;
function startup() {
  queryString = window.location.search;
  var params = new URLSearchParams(queryString);
  guid = params.get('id');
  if (!guid) {
    alert("For this site to work properly, you must browse the BSRS Website through the terminal at the North Pole, not directly. If are doing this directly, you risk not getting credit for completing the challenge.");
  };
}
function newpage(url) {
  window.location.href = url + queryString;
}
function do_presale() {
  if (!guid) {
    alert("You need to enter this site from the terminal at the North Pole, not directly. If are doing this directly, you risk not getting credit for completing the challenge.");
  } else {
    var resp = document.getElementById("response");
    var ovr = document.getElementById('overlay');
    resp.innerHTML = "";
    var cb = document.getElementById("validate").checked;
    var val = 'false'
    if (cb) {
      val = 'true'
    } else {
      ovr.style.display = 'block';
      in_trans = true;
    };
    var address = document.getElementById("wa").value;
    var proof = document.getElementById('proof').value;
    var root = '0x52cfdfdcba8efebabd9ecc2c60e6f482ab30bdc6acf8f9bd0600de83701e15f1';
    var xhr = new XMLHttpRequest();

    xhr.open('Post', 'cgi-bin/presale', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        var jsonResponse = JSON.parse(xhr.response);
        ovr.style.display = 'none';
        in_trans = false;
        resp.innerHTML = jsonResponse.Response;
      };
    };
    xhr.send(JSON.stringify({ "WalletID": address, "Root": root, "Proof": proof, "Validate": val, "Session": guid }));
  };
}
startup();
