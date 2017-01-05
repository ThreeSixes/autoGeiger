<?php
// Show the root of /api.
function showRoot() {
    // This is where we'd display the data we want to display when someone hits the root of API (hasn't sent a command).
    print("Route -> API root.");
}

/*
 * Request router
 */

// Do we have a path specified?
if (isset($_GET['t'])) {
    // Do we have anything in $_GET?
    if (strlen($_GET['t']) >= 1) {
        $x = explode("/", $_GET['t']);
        print_r($x);
    } else {
        // Show the root.
        showRoot();
    }
} else {
    // Show the root.
    showRoot();
}

?>