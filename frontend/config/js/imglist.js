var id = $.getUrlVar("id");
var imgid;
getUserImageIds = $.ajax( {
	url: "db.php",
	async: true,
	type: "POST",
	dataType: "json",
	data: {"method":"getuserimageids", "id": id }
});
getUserData = $.ajax( {
	url: "db.php",
	async: true,
	type: "POST",
	dataType: "json",
	data: {"method":"getuserdata", "id": id }
});
function resizeLightbox(){
	var lightbox_length = $('#lightbox').width() - 150*3 - 1;
	if (lightbox_length < 0){
		lightbox_length = 0;
	}
	$('.lightbox').css({"margin": "0 "+ Math.floor(lightbox_length / 6) +"px"});
}
function whatnext(e){
	$('#body').prepend( '<div id="overlay"></div>' );
	$('#overlay').fadeIn(100);
	$('#lightbox').fadeIn(100);
	resizeLightbox();
	imgid = $(this).attr("id")
};
$( window ).on("resize",resizeLightbox);
jQuery( document ).ready(function() {
	$("#cancel").on( "click", function() {
		$("#overlay, #lightbox").fadeOut(50);
	});
	$("#delete").on( "click", function() {
		if (confirm("Do you want to delete image no."+imgid+"?") == true){
			deleteImg = $.ajax( {
				url: "db.php",
				async: true,
				type: "POST",
				dataType: "json",
				data: {"method":"deletephoto", "id": imgid }
			});
			deleteImg.done(function(){
				$('#' + imgid).remove();
				$("#cancel").click();
			});
		}
	});
	$("#imglist").on( "click", "img", whatnext);	
	getUserData.done(function(data){
		$( "#name" ).html( "Photos for "+data[0].nickname+" ("+data[0].firstname+" "+data[0].lastname+")" );
	});
	getUserImageIds.done(function(data){
		for(var i = 0, l = data.length; i < l; ++i){
			$( "#imglist" ).append( '<img class="photolist" src="img.php?id='+ data[i].id +'&maxheight=600" alt="photoid: '+ data[i].id +'" id="'+ data[i].id +'">' );
		}
	});
	
});
