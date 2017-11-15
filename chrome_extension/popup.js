// Copyright (c) 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/**
 * Get the current URL.
 *
 * @param {function(string)} callback called when the URL of the current tab
 *   is found.
 */
function getCurrentTabUrl(callback) {
  // Query filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, (tabs) => {
    // chrome.tabs.query invokes the callback with a list of tabs that match the
    // query. When the popup is opened, there is certainly a window and at least
    // one tab, so we can safely assume that |tabs| is a non-empty array.
    // A window can only have one active tab at a time, so the array consists of
    // exactly one tab.
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var url = tab.url;

    // tab.url is only available if the "activeTab" permission is declared.
    // If you want to see the URL of other tabs (e.g. after removing active:true
    // from |queryInfo|), then the "tabs" permission is required to see their
    // "url" properties.
    console.assert(typeof url == 'string', 'tab.url should be a string');

    callback(url);
  });

  // Most methods of the Chrome extension APIs are asynchronous. This means that
  // you CANNOT do something like this:
  //
  // var url;
  // chrome.tabs.query(queryInfo, (tabs) => {
  //   url = tabs[0].url;
  // });
  // alert(url); // Shows "undefined", because chrome.tabs.query is async.
}



function callApi(url){
  var query = document.getElementById("userInput").value;
  console.log(query);
  console.log(url);

  var xmlhttp = new XMLHttpRequest();
  var apiUrl = "http://localhost:5000/api/v1/getbyurl?q=" + encodeURI(query) + "&url=" + encodeURI(url) + "&method=dd";

  console.log(apiUrl)

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
    for(i = 0; i < arr.length; i++) {
        console.log(arr[i].id);
    }
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
