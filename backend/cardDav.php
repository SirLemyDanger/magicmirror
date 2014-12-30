<?php
use Sabre\VObject;
use Sabre\DAV;
include 'vendor/autoload.php';
$settings = array(
    'baseUri' => "https://malte.single-point-of-failure.com:28966",
    'userName' => 'mirror',
    'password' => 'koenig\magicmirror',
    //'proxy' => 'locahost:8888',
);
$client = new DAV\Client($settings);
$method = filter_input(INPUT_GET, "method");
if (empty($method)){
    $method = "calDAV";
}
if ($method == "cardDAV")
{    
    $firstresponse = $client->propfind('/remote.php/carddav/addressbooks/'.$settings["userName"], array(
        '{DAV:}displayname'
    ),1);
    foreach ($firstresponse as $addressbook => $value) {
        if (empty($value))
        {
            continue;
        }
        $response = $client->propfind($addressbook, array(
            '{DAV:}displayname'
        ),1);
        foreach ($response as $vcardUrl => $value) {
            if ($vcardUrl == $addressbook)
            {
                continue;
            }
            $vcardresponse = $client->request('GET',$vcardUrl);
            $vcard = VObject\Reader::read($vcardresponse["body"]);
            $name = (string)$vcard->FN;
            $bday_raw =  explode("-",(string)$vcard->BDAY);
            if (!empty($bday_raw[0])){
                $bdays[$name] = mktime(0,0,0,$bday_raw[1],$bday_raw[2],$bday_raw[0])*1000;
            }
        }
    }
    $bdays["dummy"] = (time() + 86520)*1000;
    $bdays["dummy2"] = (time() + 120)*1000;
    $bdays["dummy3"] = (time() - 86200)*1000;
    $json = "{";
    $first = true;
    foreach ($bdays as $key => $value) {
        if ($first){
            $json .= "\"bdays\":[";
            $first = false;
        }else{
            $json .= ",";
        }  
        $json .="[\"{$key}\",{$value}]";
    }
    $json .= "]}";
    echo $json;
    exit();
}
elseif ($method == "calDAV")
{
    $firstresponse = $client->propfind('/remote.php/caldav/calendars/'.$settings["userName"], array(
        '{DAV:}displayname'
    ),1);
    $usermatch=[
        //owncloud id => faceRec id
        "Malte" => "malte"
    ];
    foreach ($firstresponse as $calender => $value) {
        preg_match("/\/remote\.php\/caldav\/calendars\/mirror\/(.+)_shared_by_(.+)\//", $calender, $regex_array);
        if (empty($regex_array))
        {
            continue;
        }
        $calendername = $regex_array[1];
        $user = $usermatch[$regex_array[2]];
        if (empty($user)){
            $user = "noID";
        }
       $response = $client->propfind($calender, array(
            '{DAV:}displayname'
        ),1);
        foreach ($response as $iCalItemURL => $value) {
            if ($iCalItemURL == $calender)
            {
                continue;
            }
            $iCalItemURLresponse = $client->request('GET',$iCalItemURL);
            $iCalItem = VObject\Reader::read($iCalItemURLresponse["body"]);
            echo (string)$iCalItem->VEVENT->RRULE,"\n";
        }
        
    }
    exit();
}
exit($method);