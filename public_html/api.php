<?php
// Show the root of /api.
function showRoot($addlMsg = "") {
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
    <BR />
    <?php print($addlMsg); ?>
    </BODY>
</HTML>
<?php
}

// Send the result back to the client.
function sendRes($res) {
    # If we have bad data...
    if ($res[0] == null OR $res[1] == null) {
        // For now dump the message.
        showRoot("The reason you're seeing this is an error.");
    } else {
        // Send the headers and data to the client.
        header($res[0]);
        print($res[1]);
    }
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
        
        // Set a result that will fail.
        $res = array(null, null);
        
        // Send the request to the appropriate base handler.
        switch ($routeParts[0]) {
            // Test call into API.
            case "test":
                $res[0] = "Content-Type: application/json";
                $res[1] = '{"alive": true}';
                break;
            
            // All requests served by Redis should go here.
            
            // Get the latest reading.
            case "r":
            case "latest":
                // Configure data layer.
                require 'include/dlRedis.php';
                $dlr = new dlRedis();
                
                // Send the request to the router.
                $res = $dlr->router($routeParts);
                break;
            
            // All requests served by MongoDB should go here.
            
            // Get data from DB.
            case "m":
            case "histo":
                // Configure data layer...
                require 'include/dlMongo.php';
                $dlm = new dlMongo();
                
                // Send route parts to the historical data router.
                $res = $dlm->router($routeParts);
                break;
            
            // Dafuhq?
            default:
                break;
        }
        
        // Send whatever we got to the client.
        sendRes($res);
    
    } else {
        // Show the root.
        showRoot();
    }
} else {
    // Show the root.
    showRoot();
}

?>