<?php

// Include and set up the Redis data layer...
require('include/dlRedis.php');
require('include/dlMongo.php');

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
        
        print_r($routeParts);
        
        // Send the request to the appropriate base handler.
        switch ($routeParts[0]) {
            // Test call into API.
            case "test":
                print('{"alive": true}');
                break;
            
            // All requests served by Redis should go here.
            
            // Get the latest reading.
            case "latest":
                print("At latest");
                
                // Configure data layer.
                $dlr = new dlRedis();
                
                // Send the request to the router.
                $dlr->router($routeParts);
                break;
            
            // All requests served by MongoDB should go here.
            
            // Get data from DB.
            case "histo":
                // Configure data layer...
                $dlm = new dlMongo();
                
                // Send route parts to the historical data router.
                $dlm->router($routeParts);
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