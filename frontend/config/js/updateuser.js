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

var id = $.getUrlVar("id");
getUserData = $.ajax( {
	url: "db.php",
	async: true,
	type: "GET",
	dataType: "json",
	data: {"method":"getuserdata", "id": id }
});
jQuery( document ).ready(function() {
	getUserData.done(function(data){
		$( "#firstname" ).attr( "value", data[0].firstname ).removeAttr("disabled");
		$( "#lastname" ).attr( "value", "fertig geladen :)" ).removeAttr("disabled");
		$( "#sex" ).removeAttr("disabled");
		$( "#submit" ).removeAttr("disabled");
	});
});
