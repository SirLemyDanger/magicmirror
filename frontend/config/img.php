<?php
require_once(dirname(dirname(__FILE__)) .'/db_connection.php');

function resizeImage($imagedata, $max_width, $max_height)
{
    list($orig_width, $orig_height) = getimagesizefromstring($imagedata);

    $width = $orig_width;
    $height = $orig_height;

    # taller
    if ($height > $max_height) {
        $width = ($max_height / $height) * $width;
        $height = $max_height;
    }

    # wider
    if ($width > $max_width) {
        $height = ($max_width / $width) * $height;
        $width = $max_width;
    }

    $image_p = imagecreatetruecolor($width, $height);
    $image = imagecreatefromstring($imagedata);

    imagecopyresampled($image_p, $image, 0, 0, 0, 0, $width, $height, $orig_width, $orig_height);
    imagedestroy($image);
    return $image_p;
}

$id = $mysqli->real_escape_string(filter_input(INPUT_GET, "id"));
$maxheight = $mysqli->real_escape_string(filter_input(INPUT_GET, "maxheight"));
$maxwidth = $mysqli->real_escape_string(filter_input(INPUT_GET, "maxwidth"));
$query= "SELECT imgdata,imgtype FROM images WHERE id='$id'";
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
    if ( $maxheight == false && $maxwidth == false ){
        header("Content-type: {$row['imgtype']}");
        echo $row['imgdata'];
    }else{
        header("Content-type:image/png");
        imagepng(resizeImage($row, $maxwidth, $maxheight));
    }
}
?>
