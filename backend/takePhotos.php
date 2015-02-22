<?php
header('Content-Type: text/plain; charset=utf-8');
$method = filter_input(INPUT_POST, "method");
$photocounter = filter_input(INPUT_POST, "photocounter");
$userid = filter_input(INPUT_POST, "userid");

if ( $method == "photo" && $photocounter != NULL && $userid != NULL)
{
	echo is_int($photocounter);
}
else{
	
header($_SERVER["SERVER_PROTOCOL"]." 400 Bad Request");
echo "Bad Request"
}

    // $pipe ="/tmp/pipe_faceRec";
    // if(!file_exists($pipe)){
        // umask(0);
        // posix_mkfifo( $pipe, 0666 );
    // }
    // $data = "";
    // $handle = fopen("/tmp/pipe_faceRec", "r");
    // while ($input = fread($handle, 1024)) {
            // $data .= $input;
    // }
    // fclose($handle);
    // echo $data;
    


