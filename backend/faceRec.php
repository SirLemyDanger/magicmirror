<?php
    $pipe ="/tmp/pipe_faceRec";
    if(!file_exists($pipe)){
        umask(0);
        posix_mkfifo( $pipe, 0666 );
    }
    $data = "";
    $handle = fopen("/tmp/pipe_faceRec", "r");
    while ($input = fread($handle, 1024)) {
            $data .= $input;
    }
    fclose($handle);
    echo $data;
	