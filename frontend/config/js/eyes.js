var id = $.getUrlVar("id");
var lefteye = false;
var righteye = false;
function checkSendButton(){
	if ( $("#le_x").attr("value") != "" && $("#le_y").attr("value") != "" && $("#re_x").attr("value") != "" && $("#re_y").attr("value") != "" && typeof id != 'undefined'){
			$("#submit").removeAttr( "disabled" );
	} else {
		$("#submit").attr( "disabled","disabled" );
		return false;
	}
	return true;
};
	
function sendeyes(){
	if (checkSendButton()){
		var le_x = $("#le_x").attr("value") / $("#photo").width();
		var le_y = $("#le_y").attr("value") / $("#photo").height();
		var re_x = $("#re_x").attr("value") / $("#photo").width();
		var re_y = $("#re_y").attr("value") / $("#photo").height();
		sendeyes = $.ajax( {
		url: "db.php",
		async: true,
		type: "POST",
		dataType: "json",
		data: {"method":"updateeyes", "id": id, "lefteye_x":le_x,"lefteye_y":le_y,"righteye_x":re_x,"righteye_y":re_y}
		});
	}
};

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
		checkSendButton();
	});
	//callback handler for form submit
$("#eyesform").submit(function(e)
{
    var postData = $(this).serializeArray();
    var formURL = $(this).attr("action");
    $.ajax(
    {
        url : formURL,
        type: "POST",
        data : postData,
		dataType : "json",
        success:function(data, textStatus, jqXHR)
        {
            //data: return data from server
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            //if fails     
        }
    });
    e.preventDefault(); //STOP default action
    e.unbind(); //unbind. to stop multiple form submit.
});
 
});