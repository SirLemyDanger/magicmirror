
getUserData = $.ajax( {
	url: "db.php",
	async: true,
	type: "POST",
	dataType: "json",
	data: {"method":"getallusers"}
});
jQuery( document ).ready(function() {
	$("#userlist").on( "click", "td a#delete", function(){
		if( confirm("Delete User (and all of his/her photos - not implemented yet)?") == true){
			deleteUser = $.ajax( {
				url: "db.php",
				async: true,
				type: "POST",
				dataType: "json",
				data: {"method":"deleteuser", "id": $(this).attr("name")}
			});
			deleteUser.done(function(data){
				$('#' + data[0].id).remove();
			});
		}
	});	
	getUserData.done(function(data){
		for(var i = 0, l = data.length; i < l; ++i){
			var userstring = "<tr id="+data[i].id+"\">\n"+
								"<td class=\"firstname\">"+data[i].firstname+"</td>\n"+
								"<td class=\"lastname\">"+data[i].lastname+"</td>\n"+
								"<td class=\"nickname\">"+data[i].nickname+"</td>\n"+
								"<td class=\"edit\"><a href=\"updateuser.html?id="+data[i].id+"\">edit</a>"+
								//"<td class=\"delete\"><a href=\"deleteuser.html?id="+data[i].id+"\">delete</a>"+
								"<td class=\"delete\"><a id=\"delete\" herf="" name=\""+data[i].id+"\">delete</a>"+
								"<td class=\"photo\"><a href=\"imglist.php?id="+data[i].id+"\">show photos</a>"+								
								"<td class=\"photo\"><a href=\"image_upload.html?id="+data[i].id+"\">add photo</a>"+								
							"</tr>";
			$( "#userlist" ).append( userstring );
		}
	});
});