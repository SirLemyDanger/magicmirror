<?php
require_once 'db_connection';

$id = $mysqli->real_escape_string(filter_input(INPUT_GET, "id"));
$query= "SELECT imgdata,imgtype FROM imagess WHERE id='$id'";
$result = $mysqli->query($query);
if(!$result){
    $im = ImageCreate (250,50);
    $color = ImageColorAllocate ($im, 0, 0, 0);
    $bgcolor = ImageColorAllocate ($im, 255, 255, 255);
    ImageString ($im, 2, 5, 5, $mysqli->error, $color);
    header("Content-type:image/png");
    ImagePNG($im);
}else{
    $row = $result->fetch_array(MYSQLI_ASSOC);
    header("Content-type: {$row['imgtype']}");
    echo $row['imgdata'];
}
?>
