<?php
// API request router.

// Do we have anything in $_GET?
if (len($_GET['t']) > 0) {
    $x = explode($_GET['t'], '/');
    print_r($x);
} else {
    print("Route -> API root.");
}
?>