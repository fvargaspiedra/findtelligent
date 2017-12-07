chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
  if(request.todo == "highlight"){
    var options = {
      "acrossElements": true,
    };
    var context = document.body;
    var instance = new Mark(context);
    instance.unmark();
    for(i = 0; i < request.regex.length; i++) {
      var regex = new RegExp(String(request.regex[i].regexp), 'gmi');
      instance.markRegExp(regex, options);
    }
  }
})