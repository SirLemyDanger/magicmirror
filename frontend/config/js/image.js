function checkSize(){
	if (typeof FileReader !== "undefined") {
		var size = document.getElementById('upfile').files[0].size;
		if (size > 8388608)
		{
			alert("The file must be less than 8MB");
			return false;
		}
	}
	return true;
}
var id = $.getUrlVar("id");
jQuery( document ).ready(function() {
	$( "#newphoto" ).append( '<input type="hidden" name="id" value="'+ id +'">' );
});
