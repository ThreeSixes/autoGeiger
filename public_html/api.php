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
        // Break our requested path apart by /es.
        $routeParts = explode("/", $_GET['t']);
        
        // Send the request to the appropriate base handler.
        switch ($routeParts[0]) {
            // Test call into API.
            case "test":
                print('{"alive": true}');
                break;
            
            // Get the latest reading.
            case "latest":
                // Include the Redis data layer...
                include('include/dlRedis.php');
                $dlr = new dlRedis();
                $dlr->getLast();
                break;
            
            // Get data from DB.
            case "histo":
                // Include the Mongod ata layer...
                include('include/dlMongo.php');
                $dlm = new dlMongo();
                $dlm->getLastN($_GET['t']);
                break;
            
            // Dafuhq?
            default:
                showRoot();
                break;
        }
    
    } else {
        // Show the root.
        showRoot();
    }
} else {
    // Show the root.
    showRoot();
}

?>