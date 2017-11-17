chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
  if(request.todo == "highlight"){
    console.log(request.regex);
    console.log("Hola");
    var options = {
      "acrossElements": true,
    };
    var context = document.body; // requires an element with class "context" to exist
    var instance = new Mark(context);
    //var pattern = new RegExp('Berners-Lee[^a-zA-Z0-9]*Mary[^a-zA-Z0-9]*Lee[^a-zA-Z0-9]*Woods[^a-zA-Z0-9]*Awards')
    for(i = 0; i < request.regex.length; i++) {
      var regex = new RegExp(String(request.regex[i].regexp), 'gmi');
      instance.markRegExp(regex, options); // will mark the keyword "test"
    }
  }
})