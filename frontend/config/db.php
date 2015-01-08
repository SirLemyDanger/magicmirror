<?php
$verbindung = mysql_connect ("localhost",
"mirror", "raspberry")
or die ("keine Verbindung möglich.
 Benutzername oder Passwort ist falsch");

mysql_select_db("magicmirror")
or die ("Die Datenbank existiert nicht.");

$abfrage = "SELECT firstname FROM user";
$ergebnis = mysql_query($abfrage);
while($row = mysql_fetch_object($ergebnis))
   {
   echo "$row->url <br>";
   }

?>