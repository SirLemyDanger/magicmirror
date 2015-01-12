
getUserData = $.ajax( {
	url: "db.php",
	async: true,
	type: "GET",
	dataType: "json",
	data: {"method":"getallusers"}
});
jQuery( document ).ready(function() {
	getUserData.done(function(data){
		var userstring = "<tr id="+data[0].id+"\">\n"+
							"<td class=\"firstname\">"+data[0].firstname+"</td>\n"+
							"<td class=\"lastname\">"+data[0].lastname+"</td>\n"+
							"<td class=\"nickname\">"+data[0].nickname+"</td>\n"+
						"</tr>";
		$( "#userlist" ).append( userstring );
	});
});