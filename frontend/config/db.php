<?php
require_once 'db_connection';

function newUser($firstname,$lastname,$nickname,$sex,$birthday) {
    global $mysqli;
    $id = uniqid();
    if ($nickname == "") {
        $nickname = $firstname;
    }
    if ($sex != ("male"||"female")){
        $sex = "";
    }
    $statement = $mysqli->prepare("INSERT INTO user (id, firstname, lastname, nickname, sex, birthday) VALUES (?,?,?,?,?,?)");
    $statement->bind_param('ssssss', $id, $firstname, $lastname, $nickname, $sex, $birthday);
    $statement->execute();
    $result = "";
    $statement->bind_result($result);
    $statement->fetch();
    if(!$result){
        printf("Errormessage: %s\n", $mysqli->error);
    }else{
        printf("%s\n", $mysqli->info);
    }
    return "{\"id\" : \"$id\"}";
}
function getAllUsers(){
    global $mysqli;
    $query = "SELECT id, firstname, lastname, nickname FROM user";
    $result = $mysqli->query($query);
    $data = array();
    while ($dataline = $result->fetch_array(MYSQLI_ASSOC)){
        array_push($data, $dataline);
    }
    return json_encode($data);
}
function getUserData($id){
    global $mysqli;
    $query = "SELECT id, firstname, lastname, nickname, sex, birthday FROM user WHERE id = '$id'";
    $result = $mysqli->query($query);
    if(!$result){
        printf("Errormessage: %s\n", $mysqli->error);
    }
    $data = array();
    while ($dataline = $result->fetch_array(MYSQLI_ASSOC)){
        array_push($data, $dataline);
    }
    return json_encode($data);
}
function updateUser($id,$firstname,$lastname,$nickname,$sex,$birthday) {
    global $mysqli;
    if ($nickname == "") {
        $nickname = $firstname;
    }
    if ($sex != ("male"||"female")){
        $sex = "unknown";
    }
    $query = "UPDATE user SET firstname = '$firstname', lastname = '$lastname', nickname = '$nickname', sex = '$sex', birthday = '$birthday' WHERE id = '$id';";
    $result = $mysqli->real_query($query);
    if(!$result){
        printf("Errormessage: %s\n", $mysqli->error);
    }else{
        printf("%s\n", $mysqli->info);
    }
    echo $query;
    return $result;
}
function deleteUser($id) {
    global $mysqli;
    $query = "DELETE FROM user WHERE id = '$id'";
    return $mysqli->query($query);    
}

$method = filter_input(INPUT_GET, "method");
if ($method){
    $id = $mysqli->real_escape_string(filter_input(INPUT_GET, "id"));
    $firstname = $mysqli->real_escape_string(filter_input(INPUT_GET, "firstname"));
    $lastname = $mysqli->real_escape_string(filter_input(INPUT_GET, "lastname"));
    $nickname = $mysqli->real_escape_string(filter_input(INPUT_GET, "nickname"));
    $sex = $mysqli->real_escape_string(filter_input(INPUT_GET, "sex"));
    $birthday = $mysqli->real_escape_string(filter_input(INPUT_GET, "birthday"));
    if ($method == "newuser"){
        $answer = newUser($firstname,$lastname,$nickname,$sex,$birthday);
    }elseif ($method == "getallusers"){
        $answer = getAllUsers();
    }elseif ($method == "getuserdata"){
        $answer = getUserData($id);
    }elseif ($method == "updateuser"){    
        $answer = updateUser($id,$firstname,$lastname,$nickname,$sex,$birthday);
    }elseif ($method == "deleteuser"){
        $answer = deleteuser($id);
    }
    echo $answer;
}
