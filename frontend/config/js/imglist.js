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
function whatnext(e){
	$('#body').prepend( '<div id="overlay"></div>' );
	$('#overlay').fadeIn();
	$('#lightbox').fadeIn(100);
	var lightbox_length = $('#lightbox').width() - 150*3;
	$('.lightbox').css({"marign": (lightbox_length / 6)});//.css("marignRight", lightbox_length / 6 +'px');
};
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
