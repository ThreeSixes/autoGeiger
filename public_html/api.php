<?php
print("cournt(t) = " . count($_GET['t']));

// Do we have anything in $_GET?
if (count($_GET['t']) > 1) {
    $x = explode($_GET['t'], "/");
    print_r($x);
} else {
    print("Route -> API root.");
}
?>