<?php
header('Content-Type: text/plain; charset=utf-8');
$method = filter_input(INPUT_POST, "method");
$photocounter = filter_input(INPUT_POST, "photocounter");
$userid = filter_input(INPUT_POST, "userid");

if ( $method == "photo" && is_numeric($photocounter) && $userid != False)
{
	$photocounter = intval($photocounter);
	$transfer = array(
					'method' => $method,
					'photocounter' => $photocounter,
					'userid' => $userid
	);
	$jsonTransfer = json_encode($transfer);
 
    $pipe_out ="/tmp/pipe_query";
    if(!file_exists($pipe_out)){
        umask(0);
        posix_mkfifo( $pipe, 0666 );
    }
    $handle = fopen($pipe_out, "w");
	fwrite($handle, $jsonTransfer);
    fclose($handle);
	
	$pipe_in ="/tmp/pipe_fotoout";
    if(!file_exists($pipe_in)){
        umask(0);
        posix_mkfifo( $pipe_in, 0666 );
    }
    $data = "";
    $handle = fopen($pipe_in, "r");
    while ($input = fread($handle, 1024)) {
            $data .= $input;
    }
    fclose($handle);
    echo $data;
	
}
else{
	header($_SERVER["SERVER_PROTOCOL"]." 400 Bad Request");
	echo "Bad Request";
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
    


