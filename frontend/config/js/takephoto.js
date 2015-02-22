var id = $.getUrlVar("id");

getUserData = $.ajax( {
	url: "db.php",
	async: true,
	type: "POST",
	dataType: "json",
	data: {"method":"getuserdata", "id": id }
});

jQuery( document ).ready(function() {
	getUserData.done(function(data){
		$( "#name" ).html( data[0].nickname+" ("+data[0].firstname+" "+data[0].lastname+")" );
	});
	var photcounter = $( "#photocounter" ).attr("value")
	takePhotos = $.ajax( {
		url: "db.php",
		async: true,
		type: "POST",
		dataType: "json",
		data: {"method":"photo", "photocounter": photocounterid , "userid": id}
	});
});