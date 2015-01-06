<html>
    <head>
     <title>Magic Mirror</title>
           <link rel="stylesheet" type="text/css" href="css/main.css">
           <link rel="stylesheet" type="text/css" href="css/weather-icons.css">
           <script src="js/jquery.js"></script>
           <script src="js/moment-with-locales.js"></script>
           <script src="js/main.js"></script>	
    </head>
    <body>
       
        <img id="rain" src="img/bw1.png" alt="rainbackground" >
        <div id="body">
            <div id="topleft">
                <div id="clock">
                    <div id="date"></div>
                    <div id="time"></div>
                </div>
                <div id="calender">geburtstage
                    <div id="birthdays"></div>          
                </div>
            </div>
            <div id="weather" class="weather">wetter
                <div class="windsun weather"></div>
                <div class="temp weather"></div>
                <div class="forecast weather"></div>            
            </div>
            

            <div id="kompliment">
            <?php echo "Ich hab dich sehr gern<span id=\"name\"></span>.";/*hier tolle funktion zum komplimente anzeigen. Vllt auch JS*/  ?>
            </div>
        </div>
    </body>
</html>