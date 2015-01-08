<?php
function newUser($firstname,$lastname,$nickname,$sex,$birthday) {
    $id = uniqid();
    if ($nickname == "") {
        $nickname = $firstname;
    }
    if ($sex != ("male"||"female")){
        $sex = "";
    }
    $request = "INSERT INTO user
    (id, firstname, lastname, nickname, sex, birthday)
    VALUES
    ('$id','$firstname','$lastname','$nickname','$sex','$birthday')";
    return mysql_query($request);
}
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
$method = filter_input(INPUT_POST, "method");
if ($method == "newuser"){
    $firstname = filter_input(INPUT_POST, "firstname");
    $lastname = filter_input(INPUT_POST, "lastname");
    $nickname = filter_input(INPUT_POST, "nickname");
    $firstname = filter_input(INPUT_POST, "sex");
    $birthday = filter_input(INPUT_POST, "birthday");
    newUser($firstname,$lastname,$nickname,$sex,$birthday);
}

?>