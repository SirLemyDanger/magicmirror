
jQuery( document ).ready(function() {
	$(".photolist").click(function(e){
		var img = $(this);
		var parentOffset = img.offset(); 
		var absX = Math.round( e.pageX - parentOffset.left );
		var absY = Math.round( e.pageY - parentOffset.top );
		var relX = absX / img.width();
		var relY = absY / img.height();
		
		alert("Abs:"+ absX+"/"+absY+" Rel:"+relX+"/"+relY+" Max:"+img.width()+"/"+img.height());
	});
});
