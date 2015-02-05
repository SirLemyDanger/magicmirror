jQuery( document ).ready(function() {
	$("#newuser").submit(function(e)
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