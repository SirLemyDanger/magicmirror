
getUserData = $.ajax( {
	url: "db.php",
	async: true,
	type: "GET",
	dataType: "json",
	data: {"method":"getallusers"}
});
jQuery( document ).ready(function() {
	getUserData.done(function(data){
		var userstring = "<tr id="+data[0].id+"\">"+
				"<td class=\"firstname\">"+data[0].firstname"</td>"+ 
				"<td class=\"lastname\">"+data[0].lastname+"</td>"+
				"<td class=\"nickname\">"+data[0].nickname+"</td>"+
			"</tr>";
		$( "#userlist" ).append( userstring );
	});
});