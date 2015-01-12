
getUserData = $.ajax( {
	url: "db.php",
	async: true,
	type: "GET",
	dataType: "json",
	data: {"method":"getallusers"}
});
jQuery( document ).ready(function() {
	getUserData.done(function(data){
		for(var i = 0, l = data.length; i < l; ++i){
			var userstring = "<tr id="+user.id+"\">\n"+
								"<td class=\"firstname\">"+user.firstname+"</td>\n"+
								"<td class=\"lastname\">"+user.lastname+"</td>\n"+
								"<td class=\"nickname\">"+user.nickname+"</td>\n"+
							"</tr>";
			$( "#userlist" ).append( userstring );
		}
	});
});