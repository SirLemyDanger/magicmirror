function checkSize(){
	if (typeof FileReader !== "undefined") {
		var size = document.getElementById('upfile').files[0].size;
		if (!input.files[0]) 
		{
			alert("Please select a file before clicking 'Upload'");
			return false;
		}else if (size > 8388608)
		{
			alert("The file must be less than 8MB");
			return false;
		}
	}
	return true;
}
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
		$( "#name" ).html( "Add photo for "+data[0].nickname+" ("+data[0].firstname+" "+data[0].lastname+")" );
	});
	$( "#newphoto" ).append( '<input type="hidden" name="id" value="'+ id +'">' );
});
