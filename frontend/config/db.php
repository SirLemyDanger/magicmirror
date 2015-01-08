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
function getAllUsers(){
    $request = "SELECT id, firstname, lastname, nickname FROM user";
    $query = mysql_query($request);
    while($row = mysql_fetch_object($query))
    {
        echo "$row->firstname <br>";
        #write answer into a json object
    }
}
function getUserData($id){
    $request = "SELECT id, firstname, lastname, nickname, sex, birthday FROM user WHERE id == $id";
    $query = mysql_query($request);
    while($row = mysql_fetch_object($query))
    {
        echo "$row->firstname <br>";
        #write answer into a json object
    }
}
function updateUser($id,$firstname,$lastname,$nickname,$sex,$birthday) {
    if ($nickname == "") {
        $nickname = $firstname;
    }
    if ($sex != ("male"||"female")){
        $sex = "";
    }
    $request = "UPDATE user Set"
            . "firstname = $firstname, "
            . "lastname = $lastname, "
            . "nickname = $nickname, "
            . "sex = $sex ,"
            . "birthday = $birthday "
            . "WHERE id = $id";
    return mysql_query($request);
}
function deleteUser($id) {
    $request = "DELETE FROM user WHERE id = $id";
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
$method = filter_input(INPUT_GET, "method");
if ($method == "newuser"){
    $firstname = filter_input(INPUT_GET, "firstname");
    $lastname = filter_input(INPUT_GET, "lastname");
    $nickname = filter_input(INPUT_GET, "nickname");
    $firstname = filter_input(INPUT_GET, "sex");
    $birthday = filter_input(INPUT_GET, "birthday");
    newUser($firstname,$lastname,$nickname,$sex,$birthday);
}

?>