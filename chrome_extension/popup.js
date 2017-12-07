function getCurrentTabUrl(callback) {
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, (tabs) => {
    var tab = tabs[0];
    var url = tab.url;
    console.assert(typeof url == 'string', 'tab.url should be a string');
    callback(url);
  });
}

function callApi(url){
  var query = document.getElementById("userInput").value;
  var xmlhttp = new XMLHttpRequest();
  var apiUrl = "http://localhost:5000/api/v1/getbyurl?q=" + encodeURI(query) + "&url=" + encodeURI(url) + "&method=dd";
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var myArr = JSON.parse(this.responseText);
      myFunction(myArr);
    }
  };
  xmlhttp.open("GET", apiUrl, true);
  xmlhttp.send();
  function myFunction(arr) {
    var out = "";
    var i;
    var re;
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
      chrome.tabs.sendMessage(tabs[0].id, {todo: "highlight", regex: arr})
    })
  }
}

window.onload=function(){
  document.getElementById("submitQuery").addEventListener("click", () => { getCurrentTabUrl((url) => { callApi(url) }); });
  document.getElementById("userInput").addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        document.getElementById("submitQuery").click();
    }
  });
}
