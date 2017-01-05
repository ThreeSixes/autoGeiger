<?php

if (isset($_GET['t'])) {
    print("I can haz t!\n");
}
// Do we have anything in $_GET?
if (strlen($_GET['t']) >= 1) {
    $x = explode($_GET['t'], "/");
    print_r($x);
} else {
    print("Route -> API root.");
}
?>