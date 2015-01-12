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
		$( "#id" ).attr( "value", data[0].id );
		$( "#firstname" ).attr( "value", data[0].firstname ).removeAttr("disabled");
		$( "#lastname" ).attr( "value", data[0].lastname ).removeAttr("disabled");
		$( "#nickname" ).attr( "value", data[0].nickname ).removeAttr("disabled");
		if (data[0].sex == "male"){
			$( "#male" ).attr( "checked", "checked");
		}else if (data[0].sex == "female"){
			$( "#female" ).attr( "checked", "checked");
		//}else if (data[0].sex == other){
		//	$( "#other" ).attr( "checked", "checked");
		}
		$( "#sex" ).removeAttr("disabled");
		$( "#birthday" ).attr( "value", data[0].birthday ).removeAttr("disabled");
		$( "#submit" ).removeAttr("disabled");
	});
});
