<?php

$mysqli = mysqli_init();

function newUser($firstname,$lastname,$nickname,$sex,$birthday) {
    $id = uniqid();
    if ($nickname == "") {
        $nickname = $firstname;
    }
    if ($sex != ("male"||"female")){
        $sex = "";
    }
    $query = "INSERT INTO user
    (id, firstname, lastname, nickname, sex, birthday)
    VALUES
    ('$id','$firstname','$lastname','$nickname','$sex','$birthday')";
    return $mysqli->query($query);
}
function getAllUsers(){
    $query = "SELECT id, firstname, lastname, nickname FROM user";
    $result = $mysqli->query($query);
    $data = $result->fetch_all(MYSQLI_ASSOC);
    var_dump($data);
    var_dump(json_encode($data));
    return json_encode($data);
}
function getUserData($id){
    $query = "SELECT id, firstname, lastname, nickname, sex, birthday FROM user WHERE id == $id";
    $result = $mysqli->query($query);
    $data = $result->fetch_all(MYSQLI_ASSOC);
    echo $data;
    return json_encode($data);
}
function updateUser($id,$firstname,$lastname,$nickname,$sex,$birthday) {
    if ($nickname == "") {
        $nickname = $firstname;
    }
    if ($sex != ("male"||"female")){
        $sex = "";
    }
    $query = "UPDATE user Set"
            . "firstname = $firstname, "
            . "lastname = $lastname, "
            . "nickname = $nickname, "
            . "sex = $sex ,"
            . "birthday = $birthday "
            . "WHERE id = $id";
    return $mysqli->query($query);
}
function deleteUser($id) {
    $query = "DELETE FROM user WHERE id = $id";
    return $mysqli->query($query);    
}
$mysqli->real_connect ("localhost",
"mirror", "raspberry", "magicmirror")
or die ("keine Verbindung zur Datenbank möglich.");

getAllUsers();
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