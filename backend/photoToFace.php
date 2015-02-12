<?php

$ids = array('22','23','24');
function faceForID($ids){
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
	fwrite($handle, $jsonTransfer)
    fclose($handle);
	}
faceForID($ids);