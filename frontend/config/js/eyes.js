var id = $.getUrlVar("id");
var lefteye = false;
var righteye = false;
jQuery( document ).ready(function() {
	if (typeof id != 'undefined'){
		$('#photo').attr("src", "img.php?id=" + id);
		$('#photo').attr("alt", "photoid=" + id);
	}
	$("#photo").click(function(e){
		var img = $(this);
		var parentOffset = img.offset(); 
		var absX = Math.round( e.pageX - parentOffset.left );
		var absY = Math.round( e.pageY - parentOffset.top );
		var relX = absX / img.width();
		var relY = absY / img.height();
		if (lefteye == true){
			$("#le_x").attr("value",absX);
			$("#le_y").attr("value",absY);
		}else if (righteye == true){
			$("#re_x").attr("value",absX);
			$("#re_y").attr("value",absY);
		}
		lefteye = false;
		righteye = false;
	});
});