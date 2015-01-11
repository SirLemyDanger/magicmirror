<?php
// terminal -> GET
foreach ($argv as $arg) {
    $e=explode("=",$arg);
    if(count($e)==2)
        $_GET[$e[0]]=$e[1];
    else   
        $_GET[$e[0]]=0;
}

$mysqli = mysqli_init();

function newUser($firstname,$lastname,$nickname,$sex,$birthday) {
    global $mysqli;
    $id = uniqid();
    if ($nickname == "") {
        $nickname = $firstname;
    }
    if ($sex != ("male"||"female")){
        $sex = "";
    }
    $query = "INSERT INTO 'user' ('id', 'firstname', 'lastname', 'nickname') VALUES ('$id','$firstname','$lastname','$nickname')";
    $result = $mysqli->query($query);
    if(!$result){
        printf("Errormessage: %s\n", $mysqli->error);
    }else{
        printf("%s\n", $mysqli->info);
    }
    echo $query;
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
//$mysqli->real_connect ("localhost",
//"mirror", "raspberry", "magicmirror")
//or die ("keine Verbindung zur Datenbank möglich.");
if (!$mysqli) {
    die('mysqli_init failed');
}

if (!$mysqli->options(MYSQLI_INIT_COMMAND, 'SET AUTOCOMMIT = 0')) {
    die('Setting MYSQLI_INIT_COMMAND failed');
}

if (!$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5)) {
    die('Setting MYSQLI_OPT_CONNECT_TIMEOUT failed');
}

if (!$mysqli->real_connect ("localhost", "mirror", "raspberry", "magicmirror")) {
    die('Connect Error (' . mysqli_connect_errno() . ') '
            . mysqli_connect_error());
}
/* change character set to utf8 */
if (!$mysqli->set_charset("utf8")) {
    printf("Error loading character set utf8: %s\n", $mysqli->error);
}
//} else {
//    printf("Current character set: %s\n", $mysqli->character_set_name());
//}

//echo 'Success... ' . $mysqli->host_info . "\n";

$method = filter_input(INPUT_GET, "method");
if ($method == "newuser"){
    $firstname = filter_input(INPUT_GET, "firstname");
    $lastname = filter_input(INPUT_GET, "lastname");
    $nickname = filter_input(INPUT_GET, "nickname");
    $sex = filter_input(INPUT_GET, "sex");
    $birthday = filter_input(INPUT_GET, "birthday");
    $answer = newUser($firstname,$lastname,$nickname,$sex,$birthday);
}elseif ($method == "getallusers"){
    $answer = getAllUsers();
}elseif ($method == "getuserdata"){
    $id = filter_input(INPUT_GET, "id");
    $answer = getUserData($id);
}elseif ($method == "updateuser"){
    $id = filter_input(INPUT_GET, "id");
    $firstname = filter_input(INPUT_GET, "firstname");
    $lastname = filter_input(INPUT_GET, "lastname");
    $nickname = filter_input(INPUT_GET, "nickname");
    $sex = filter_input(INPUT_GET, "sex");
    $birthday = filter_input(INPUT_GET, "birthday");
    $answer = updateUser($id,$firstname,$lastname,$nickname,$sex,$birthday);
}elseif ($method == "deleteuser"){
    $id = filter_input(INPUT_GET, "id");
    $answer = deleteuser($id);
}
echo $answer;

?>