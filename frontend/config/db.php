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
$db_connection= mysql_connect ("localhost",
"mirror", "raspberry")
or die ("keine Verbindung möglich.
 Benutzername oder Passwort ist falsch");

mysql_select_db("magicmirror")
or die ("Die Datenbank existiert nicht.");

$method = filter_input(INPUT_GET, "method");
if ($method == "newuser"){
    $firstname = filter_input(INPUT_GET, "firstname");
    $lastname = filter_input(INPUT_GET, "lastname");
    $nickname = filter_input(INPUT_GET, "nickname");
    $sex = filter_input(INPUT_GET, "sex");
    $birthday = filter_input(INPUT_GET, "birthday");
    $answer = newUser($firstname,$lastname,$nickname,$sex,$birthday);
}
elseif ($method == "getallusers"){
    $answer = getAllUsers();
}
elseif ($method == "getuserdata"){
    $id = filter_input(INPUT_GET, "id");
    $answer = getUserData($id);
}
elseif ($method == "newuser"){
    $id = filter_input(INPUT_GET, "id");
    $firstname = filter_input(INPUT_GET, "firstname");
    $lastname = filter_input(INPUT_GET, "lastname");
    $nickname = filter_input(INPUT_GET, "nickname");
    $sex = filter_input(INPUT_GET, "sex");
    $birthday = filter_input(INPUT_GET, "birthday");
    $answer = updateUser($id,$firstname,$lastname,$nickname,$sex,$birthday);
}
elseif ($method == "getuserdata"){
    $id = filter_input(INPUT_GET, "id");
    $answer = deleteuser($id);
}
echo $answer;
?>