var id = $.getUrlVar("id");
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
	var lightbox_length = Math.floor($('#lightbox').width() - 150*3);
	if (lightbox_length < 0){
		lightbox_length = 0;
	}
	$('.lightbox').css({"margin": "0 "+ lightbox_length / 6 +"px"});
}
function whatnext(e){
	$('#body').prepend( '<div id="overlay"></div>' );
	$('#overlay').fadeIn();
	$('#lightbox').fadeIn(100);
	resizeLightbox();
};
$( window ).on("resize",resizeLightbox);
jQuery( document ).ready(function() {
	$("#imglist").on( "click", "img", whatnext);
	
	getUserData.done(function(data){
		$( "#name" ).html( "Photos for "+data[0].nickname+" ("+data[0].firstname+" "+data[0].lastname+")" );
	});
	getUserImageIds.done(function(data){
		for(var i = 0, l = data.length; i < l; ++i){
			$( "#imglist" ).append( '<img class="photolist" src="img.php?id='+ data[i].id +'" alt="photoid: '+ data[i].id +'" id="'+ data[i].id +'">' );
		}
	});
	
});
