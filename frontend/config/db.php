<?php
$verbindung = mysql_connect ("localhost",
"mirror", "raspberry")
or die ("keine Verbindung möglich.
 Benutzername oder Passwort ist falsch");

mysql_select_db("magicmirror")
or die ("Die Datenbank existiert nicht.");

$abfrage = "SELECT firstname FROM user";
$query = mysql_query($abfrage);
if(!$query){
	echo mysql_error();
	}
else{   
        echo $query;
	while($row = mysql_fetch_object($query))
	{
		echo "$row->firstname <br>";
	}
	echo "toll";
	}


?>