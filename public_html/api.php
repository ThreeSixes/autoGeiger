<?php
// API request router.

// Do we have anything in $_GET?
if (len($_GET) > 0) {
    $x = explode($_GET, '/');
    print_r($x);
} else {
    print("Route -> API root.");
}
?>