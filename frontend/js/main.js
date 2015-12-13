moment.locale("de");
var facePipeMutex = 0;
var faceDataRequest;

var weatherParams = {
    'q':'Darmstadt,de',
    'units':'metric',
    'lang':'de',
	'APPID':'821d72209366eaeb1a7d5adec6c6df5c'
};
var birthdays= {};
var maxBday = 10;

jQuery.fn.updateWithText = function(text, speed)
{
	var dummy = $('<div/>').html(text);

	if ($(this).html() !== dummy.html())
	{
		$(this).fadeOut(speed/2, function() {
			$(this).html(text);
			$(this).fadeIn(speed/2, function() {
				//done
			});
		});
	}
};
jQuery.fn.outerHTML = function(s) {
    return s
        ? this.before(s).remove()
        : jQuery("<p>").append(this.eq(0).clone()).html();
};

function roundVal(temp)
{
    return Math.round(temp * 10) / 10;
}

function kmh2beaufort(kmh)
{
	var speeds = [1, 5, 11, 19, 28, 38, 49, 61, 74, 88, 102, 117, 1000];
	for (var beaufort in speeds) {
		var speed = speeds[beaufort];
		if (speed > kmh) {
			return beaufort;
		}
	}
	return 12;
}

jQuery( document ).ready(function() {
	$( "#body" ).addClass( "test" );
	$( ".test" ).click( function() {
		$( this ).hide( 4000 ).delay( 1000 ).fadeIn ( 400 );
	});
	(function updateTime()
	{
            var now = moment();
            var date = now.format('LLLL').split(' ',4);
            date = date[0] + ' ' + date[1] + ' ' + date[2] + ' ' + date[3];

            $( "#date" ).html(date);
            $( "#time" ).html(now.format('HH') + ':' + now.format('mm') + '<span class="sec">:'+now.format('ss')+'</span>');

            setTimeout(function() {
                    updateTime();
            }, 1000);
	})();
	
	// receive person ids and genders from face recognition
	(function updateFaceData()
	{
		if (facePipeMutex !== 0){
			return;
		}
		facePipeMutex++;
                
		var stop = false;
		faceDataRequest = $.ajax( {
			url: "../backend/faceRec.php",
			async: true,
			type: "POST",
            //cache: false,
			dataType: "json"
		});
		faceDataRequest.done(function(data){
			var numOfFaces;
			if (data === null || data === ""){
				numOfFaces = 0;
				$( "#name" ).html("");
			}else{
				if (data[0].typ === "stop"){ 
						stop = true;
						return;
				}
			numOfFaces = data.length;
			$( "#name" ).html( "" )
			for (var i = 0; i < numOfFaces; i++)
				if (data[i].typ == "sex")
				{
					$( "#name" ).append("Geschlecht: "+ data[i].prediction+ " confidence: " +data[i].confidence+ "<br>");
				}
				else if ( data[i].typ == "person")
				{
					getUserData = $.ajax( {
						url: "db.php",
						async: true,
						type: "POST",
						dataType: "json",
						data: {"method":"getuserdata", "id":data[i].prediction}
					});
					getUserData.done(function(user){
						$( "#name" ).append("<br>Hallo "+ user[0].firstname );
					});
					
				}
			}
		});
		faceDataRequest.fail(function(textStatus, errorThrown){
			if (textStatus !== "timeout"){
				//alert("Anfrage an Gesichtserkennung ist gescheitert. Fehler:" + errorThrown);
			}
		});
		faceDataRequest.complete(function(){
			facePipeMutex--;
			if (stop === true){return;}
			updateFaceData();
		});
	})();
        (function updateCurrentWeather()
	{
		var iconTable = {
			'01d':'wi-day-sunny',
			'02d':'wi-day-cloudy',
			'03d':'wi-cloudy',
			'04d':'wi-cloudy-windy',
			'09d':'wi-showers',
			'10d':'wi-rain',
			'11d':'wi-thunderstorm',
			'13d':'wi-snow',
			'50d':'wi-fog',
			'01n':'wi-night-clear',
			'02n':'wi-night-cloudy',
			'03n':'wi-night-cloudy',
			'04n':'wi-night-cloudy',
			'09n':'wi-night-showers',
			'10n':'wi-night-rain',
			'11n':'wi-night-thunderstorm',
			'13n':'wi-night-snow',
			'50n':'wi-night-alt-cloudy-windy'
		};
		var currentWeather = $.ajax({
                    dataType: "json",
                    url: 'http://api.openweathermap.org/data/2.5/weather',
                    data: weatherParams
                    });
                currentWeather.done(function(json){
			var temp = roundVal(json.main.temp);
			var temp_min = roundVal(json.main.temp_min);
			var temp_max = roundVal(json.main.temp_max);

			var wind = roundVal(json.wind.speed);

			var iconClass = iconTable[json.weather[0].icon];
			var icon = $('<span/>').addClass('icon').addClass('dimmed').addClass('wi').addClass(iconClass);
                        $('.temp').updateWithText(icon.outerHTML() +temp+'&deg;', 1000);

			// var forecast = 'Min: '+temp_min+'&deg;, Max: '+temp_max+'&deg;';
			// $('.forecast').updateWithText(forecast, 1000);

			var now = new Date();
			var sunrise = new Date(json.sys.sunrise*1000).toTimeString().substring(0,5);
			var sunset = new Date(json.sys.sunset*1000).toTimeString().substring(0,5);

			var windString = '<span class="wi wi-strong-wind xdimmed"></span> ' + kmh2beaufort(wind) ;
			var sunString = '<span class="wi wi-sunrise xdimmed"></span> ' + sunrise;
			if (json.sys.sunrise*1000 < now && json.sys.sunset*1000 > now) {
				sunString = '<span class="wi wi-sunset xdimmed"></span> ' + sunset;
			}
			$('.windsun').updateWithText(windString+' '+sunString, 1000);

                });
                currentWeather.fail(function(textStatus, errorThrown){
					console.log("Anfrage CurrWeather ist gescheitert. %o %o:" ,textStatus, errorThrown);
                    //alert("Anfrage CurrWeather ist gescheitert. Fehler:" +textStatus+" "+errorThrown);
                });

		setTimeout(function() {
			updateCurrentWeather();
		}, 300000);
	})();
	(function updateWeatherForecast()
	{
			$.getJSON('http://api.openweathermap.org/data/2.5/forecast', weatherParams, function(json, textStatus) {
			var forecastData = {};
			for (var i in json.list) {
				var forecast = json.list[i];
				var dateKey  = forecast.dt_txt.substring(0, 10);
				if (forecastData[dateKey] == undefined) {
					forecastData[dateKey] = {
						'timestamp':forecast.dt * 1000,
						'temp_min':forecast.main.temp,
						'temp_max':forecast.main.temp
					};
				} else {
					forecastData[dateKey]['temp_min'] = (forecast.main.temp < forecastData[dateKey]['temp_min']) ? forecast.main.temp : forecastData[dateKey]['temp_min'];
					forecastData[dateKey]['temp_max'] = (forecast.main.temp > forecastData[dateKey]['temp_max']) ? forecast.main.temp : forecastData[dateKey]['temp_max'];
				}
			}
			var forecastTable = $('<table />').addClass('forecast-table').css("float","right");
			var opacity = 1;
			for (var i in forecastData) {
				var forecast = forecastData[i];
				var dt = new Date(forecast.timestamp);
				var row = $('<tr />').css('opacity', opacity);
				row.append($('<td/>').addClass('day').html(moment.weekdaysShort(dt.getDay())));
				row.append($('<td/>').addClass('temp-max').html(roundVal(forecast.temp_max)));
				row.append($('<td/>').addClass('temp-min').html(roundVal(forecast.temp_min)));
				forecastTable.append(row);
				opacity -= 0.155;
			}
			$('.forecast').updateWithText(forecastTable, 1000);
		});
		setTimeout(function() {
			updateWeatherForecast();
		}, 3600000);
	})();
        (function updateBirthdayData()
	{
            var getBirthdays = $.ajax({
                dataType: "json",
                url: "../backend/cardDav.php",
                async: true,
                //cache: false,
                data: {"method":"cardDAV"},
                type: "GET"
                });
            getBirthdays.done(function(json){
                birthdays = json;
            });
            getBirthdays.fail(function(textStatus, errorThrown){
                alert("Anfrage getBirthdays ist gescheitert. Fehler:" +textStatus+" "+errorThrown);
            });

            setTimeout(function() {
                    updateBirthdayData();
            }, 21600000);
	})();
        (function updateBirthdays()
	{   
            var speedup = false;
            if (Object.getOwnPropertyNames(birthdays).length !== 0 )
            {
                var now = new Date();
                var year = now.getFullYear();
                birthdays.bdays.sort(function(a,b) {
					//sort birthdays
                    var date_a = new Date(a[1]);
                    var date_b = new Date(b[1]);
                    if ((now.getMonth()===date_a.getMonth())&&(now.getDate()===date_a.getDate())){
                        date_a = now;
                    }else{
                        date_a.setFullYear(year);
                        if (date_a-now < 0 ){
                            date_a.setFullYear(year+1);
                        }
                    }
                    if ((now.getMonth()===date_b.getMonth())&&(now.getDate()===date_b.getDate())){
                        date_b = now;
                    }else{
                        date_b.setFullYear(year);
                        if (date_b-now < 0 ){
                            date_b.setFullYear(year+1);
                        }
                    }
                    return (date_a - now) - (date_b - now);});
                var bdayTable = $('<table />').addClass(".bday");
                var opacity = 1;
                if (maxBday > birthdays.bdays.length){
                    maxBday = birthdays.bdays.length;
                }
                for (var i=0; i<maxBday; i++) {
                    var birthday = new Date(birthdays.bdays[i][1]);
                    var today = false;
					var diff;
                    if ((now.getMonth()===birthday.getMonth())&&(now.getDate()===birthday.getDate())){
                        today = true;
                    }else{
                        birthday.setFullYear(year);
						diff = birthday - now;                        
                        if (diff < 0 ){
                            birthday.setFullYear(year+1);
                        }
						if ((0 < diff) && (diff <= 105000)){
                            speedup = true;
                        }
						if (diff > (22*60*60*1000)){//22hours
                            birthday.setHours(now.getHours());
							birthday.setMinutes(now.getMinutes());
							birthday.setSeconds(now.getSeconds());
                        }
                    }
                    var row = $('<tr />').css('opacity', opacity);
                    row.append($('<td/>').addClass('name').html(birthdays.bdays[i][0]));
                    if (today) {
                        row.append($('<td/>').addClass('timeFromNow').html("heute"));
                    }else{
                        var momentbday = moment(birthday);
                        row.append($('<td/>').addClass('timeFromNow').html(momentbday.fromNow()));
                    }
                    bdayTable.append(row);
                    opacity -= 0.055;
                }
                $("#birthdays").updateWithText(bdayTable, 1000);
            }
            var nowafter = new Date(); 
            if (speedup === true){
                var nextcall = 1000 - (nowafter - now);
            }else{
                var nextcall = 60000;
            }
            
            setTimeout(function() {
                    updateBirthdays();
            }, nextcall);
	})();
});
