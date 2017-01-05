<?php
// API request router.
print(count($_GET) . "\n");
print(count($_GET['t']) . "\n");
// Do we have anything in $_GET?
if (count($_GET['t']) > 0) {
    $x = explode($_GET['t'], '/');
    print_r($x);
} else {
    print("Route -> API root.");
}
?>