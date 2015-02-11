<?php
require_once(realpath(dirname(__FILE__) . '/db_connection.php'));

function caching_headers ($filename, $timestamp) {
    $gmt_mtime = gmdate('r', $timestamp);
    header('ETag: "'.md5($timestamp.$filename).'"');
    header('Last-Modified: '.$gmt_mtime);
    header('Cache-Control: public');

    if(isset($_SERVER['HTTP_IF_MODIFIED_SINCE']) || isset($_SERVER['HTTP_IF_NONE_MATCH'])) {
        if ($_SERVER['HTTP_IF_MODIFIED_SINCE'] == $gmt_mtime || str_replace('"', '', stripslashes($_SERVER['HTTP_IF_NONE_MATCH'])) == md5($timestamp.$filename)) {
            header('HTTP/1.1 304 Not Modified');
            exit();
        }
    }
}
$id = $mysqli->real_escape_string(filter_input(INPUT_GET, "id"));
$type = $mysqli->real_escape_string(filter_input(INPUT_GET, "type"));
if ($type == "face"){
    $query = "SELECT imgdata, imgtype, last_modified FROM faces WHERE id='$id'";
}else{
    $type = "photo";
    $query= "SELECT imgdata, imgtype, last_modified FROM images WHERE id='$id'";
}
$result = $mysqli->query($query);
if(!$result){
    $im = ImageCreate (250,50);
    $color = ImageColorAllocate ($im, 0, 0, 0);
    ImageString ($im, 2, 5, 5, $mysqli->error, $color);
    header("Content-type:image/png");
    ImagePNG($im);
    exit();
}else{
    $row = $result->fetch_array(MYSQLI_ASSOC);
    $filename = $id . $type;
    caching_headers($id,$row['last_modified']);
    header("Content-type: {$row['imgtype']}");
    echo $row['imgdata'];
}
?>
