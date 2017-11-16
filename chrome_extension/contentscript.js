chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
  if(request.todo == "highlight"){
    console.log(request.regex);
    console.log("Hola");
  }
})