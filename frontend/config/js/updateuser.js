$.extend({
  getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});
({
	getUserData = $.ajax( {
		url: "db.php",
		async: true,
		type: "GET",
		//chace: false,
		dataType: "json"
		data: {"method":"getuserdata"},
	});
	getUserData.done(function(data){
		$["#firstname"].attr( "value", "fertig geladen :)" ).removeAttr("disabled");
		$["#lastname"].attr( "value", "fertig geladen :)" ).removeAttr("disabled");
		$["#sex"].removeAttr("disabled");
		$["#submit"].removeAttr("disabled");
	});
});