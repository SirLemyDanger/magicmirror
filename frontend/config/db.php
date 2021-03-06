<?php
require_once(realpath(dirname(__FILE__) . '/db_connection.php'));
header('Content-Type: text/plain; charset=utf-8');

function faceForIDs($ids){
	# generate face-picture from photo (external python program)
	if (!is_array($ids)){
		$ids = array($ids);
	}
	$transfer = array('ids' => $ids);
	$jsonTransfer = json_encode($transfer);
		
    // #input pipe
    // $pipe_in ="/tmp/pipe_faceIDs_back";
    // if(!file_exists($pipe_in)){
        // umask(0);
        // posix_mkfifo( $pipe, 0666 );
    // }
	#input pipe
    $pipe_out ="/tmp/pipe_faceIDs";
    if(!file_exists($pipe_out)){
        umask(0);
        posix_mkfifo( $pipe, 0666 );
    }
    $handle = fopen("/tmp/pipe_faceIDs", "w");
	fwrite($handle, $jsonTransfer);
    fclose($handle);
}
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
    }
    return "[{\"id\":\"$mysqli->insert_id\"}]";
}
function deleteUser($id) {
    global $mysqli;
    $query = "DELETE FROM user WHERE id = '$id'";
    $result = $mysqli->query($query);
    if (!result){
            return $mysqli->error;
    }
    return "[{\"id\" : \"$id\"}]"; 
}
function getUserImageIds($userid){
    global $mysqli;
    $query = "SELECT id FROM images WHERE userid = '$userid'";
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
function checkFile(&$mime) {
    try {   
        // Undefined | Multiple Files | $_FILES Corruption Attack
        // If this request falls under any of them, treat it invalid.
        if (
            !isset($_FILES['upfile']['error']) ||
            is_array($_FILES['upfile']['error'])
        ) {
            throw new RuntimeException('Invalid parameters.');
        }
        // Check $_FILES['upfile']['error'] value.
        switch ($_FILES['upfile']['error']) {
            case UPLOAD_ERR_OK:
                break;
            case UPLOAD_ERR_NO_FILE:
                throw new RuntimeException('No file sent.');
            case UPLOAD_ERR_INI_SIZE:
            case UPLOAD_ERR_FORM_SIZE:
                throw new RuntimeException('Exceeded filesize limit.');
            default:
                throw new RuntimeException('Unknown errors.');
        }
        // You should also check filesize here.
        if ($_FILES['upfile']['size'] > 8388608) {
            throw new RuntimeException('Exceeded filesize limit.');
        }
        // DO NOT TRUST $_FILES['upfile']['mime'] VALUE !!
        // Check MIME Type by yourself.
        $finfo = new finfo(FILEINFO_MIME_TYPE);
        $mime = $finfo->file($_FILES['upfile']['tmp_name']);
        if (false === $ext = array_search(
            $finfo->file($_FILES['upfile']['tmp_name']),
            array(
                'jpg' => 'image/jpeg',
                'png' => 'image/png',
                'gif' => 'image/gif',
            ),
            true
        )) {
            throw new RuntimeException('Invalid file format.');
        }
        // You should name it uniquely.
        // DO NOT USE $_FILES['upfile']['name'] WITHOUT ANY VALIDATION !!
        // On this example, obtain safe unique name from its binary data.
    //    if (!move_uploaded_file(
    //        $_FILES['upfile']['tmp_name'],
    //        sprintf('./uploads/%s.%s',
    //            sha1_file($_FILES['upfile']['tmp_name']),
    //            $ext
    //        )
    //    )) {
    //        throw new RuntimeException('Failed to move uploaded file.');
    //    }

        return true;

        } catch (RuntimeException $e) {
        return $e->getMessage();
    }   
}
function uploadNewPhoto($userid) {
    global $mysqli;
    if (true != $check_result = checkFile($mime)){
        return $check_result;
    }
    if(is_uploaded_file($_FILES['upfile']['tmp_name'])) {
            $image = $_FILES['upfile']['tmp_name'];
            $data = $mysqli->real_escape_string(file_get_contents($image));
            $query = "INSERT INTO images (imgdata, imgtype, userid) VALUES ('$data', '$mime', '$userid')";
            $result = $mysqli->query($query);
            if(!$result){
                printf("Errormessage: %s\n", $mysqli->error);
            }else{
                return "[{\"id\": {$mysqli->insert_id} }]";
            }
    }else{
        return "is_uploaded_file is false. File:" . $_FILES['upfile']['tmp_name'] . $_FILES['upfile']['error'] . "var dump " . var_dump($_FILES);
    }
    return "ok";
}
function deletePhoto($id) {
    global $mysqli;
    $query = "DELETE FROM images WHERE id = '$id'";
    return $mysqli->query($query);  
}
function updateEyes($fotoid,$lefteye_x,$lefteye_y,$righteye_x,$righteye_y){
    global $mysqli;
    $query = "UPDATE images SET lefteye_x = '$lefteye_x', lefteye_y = '$lefteye_y', righteye_x = '$righteye_x', righteye_y = '$righteye_y' WHERE id = '$fotoid';";
    $result = $mysqli->real_query($query);
    if(!$result){
        printf("Errormessage: %s\n", $mysqli->error);
        return false;
    }
	faceForIDs($fotoid);
    return true;
}
$answer = "[\"Error. No function executed\"]";
$method = filter_input(INPUT_POST, "method");
if ($method){
    $id = $mysqli->real_escape_string(filter_input(INPUT_POST, "id"));
    $firstname = $mysqli->real_escape_string(filter_input(INPUT_POST, "firstname"));
    $lastname = $mysqli->real_escape_string(filter_input(INPUT_POST, "lastname"));
    $nickname = $mysqli->real_escape_string(filter_input(INPUT_POST, "nickname"));
    $sex = $mysqli->real_escape_string(filter_input(INPUT_POST, "sex"));
    $birthday = $mysqli->real_escape_string(filter_input(INPUT_POST, "birthday"));
    $lefteye_x = $mysqli->real_escape_string(filter_input(INPUT_POST, "lefteyeX"));
    $lefteye_y = $mysqli->real_escape_string(filter_input(INPUT_POST, "lefteyeY"));
    $righteye_x = $mysqli->real_escape_string(filter_input(INPUT_POST, "righteyeX"));
    $righteye_y = $mysqli->real_escape_string(filter_input(INPUT_POST, "righteyeY"));
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
    }elseif ($method == "getuserimageids"){
        $answer = getUserImageIds($id);
    }elseif ($method == "newphoto"){
        $answer = uploadNewPhoto($id);
    }elseif ($method == "deletephoto"){
        $answer = deletePhoto($id);
    }elseif ($method == "updateeyes"){
        $answer = updateEyes($id,$lefteye_x,$lefteye_y,$righteye_x,$righteye_y);
    }else{
        echo "\"$method\" is an unknown method";
    }
    echo $answer;
    return;
}
header($_SERVER["SERVER_PROTOCOL"]." 400 Bad Request");
echo "no method";
return;
