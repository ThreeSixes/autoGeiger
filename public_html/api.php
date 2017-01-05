<?php
// Show the root of /api.
function showRoot() {
?>
<HTML>
    <HEAD>
        <TITLE>PUBROW</TITLE>
    </HEAD>
    <BODY>
Endpoints:
        <PRE>
<?php print($_SERVER['HTTP_HOST']); ?>/api: You are here.
 - /histo: Get historical readings.
 - /latest: Get the latest readings.
 - /test: Test webserver.
        </PRE>
    </BODY>
</HTML>
<?php
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
                header("Content-Type: application/json");
                print('{"alive": true}');
                break;
            
            // All requests served by Redis should go here.
            
            // Get the latest reading.
            case "r":
            case "latest":
                // Configure data layer.
                require 'include/dlRedis.php';
                $dlr = new dlRedis();
                
                // Send the request to the router.
                $dlr->router($routeParts);
                break;
            
            // All requests served by MongoDB should go here.
            
            // Get data from DB.
            case "m":
            case "histo":
                // Configure data layer...
                require 'include/dlMongo.php';
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