chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
  if(request.todo == "highlight"){
    console.log(request.regex);
    console.log("Hola");
    var context = document.body; // requires an element with class "context" to exist
    var instance = new Mark(context);
    instance.markRegExp(/computer/gmi); // will mark the keyword "test"
  }
})