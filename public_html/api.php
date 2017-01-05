<?php
// Set this so we don't break our includes.
define("LOADFROMAPI", True);

// Show the root of /api.
function showRoot($addlMsg = "") {
?>
<HTML>
    <HEAD>
        <TITLE>PUBROW</TITLE>
    </HEAD>
    <BODY>
Quick-and-dirty documentation:
        <PRE>
== API ==
<?php print($_SERVER['HTTP_HOST']); ?>/api: You are here.
 - /histo: Get historical readings. This is not yet implemented.
 - /latest: Get the latest readings.
 - /m: Database-specific commands.
   - /test: Make sure database is reachable.
 - /r: Que-specific commands.
   - /test: Make sure queue is alive.
 - /test: Test webserver.
 
 == Record format ==
 Records from experiment are in JSON format as follows:
 {'humidRH': 29.57, 'dts': '2017-01-05 04:46:03.211875', 'fastFull': True, 'slowFull': True, 'humidTemp': 16.99, 'slowCpm': 0.0,
  'alarm': False, 'baroPres': 101836.0, 'cpsGood': False, 'cps': 0, 'baroTemp': 17.39, 'fastCpm': 0.0}
 
 Fields are as follows:
 {'humidRH': nn.nn, # Humdity in %rH
  'dts': 'YYYY-MM-DD HH:MM:SS.ffffff', # UTC timestamp
  'fastFull': [True/False], # Fast average of counts per second (averaged over 4 sec)
  'slowFull': [True/False], # Fast average of counts per second (averaged over 22 sec)
  'humidTemp': nn.nn, # Humidity sensor's temperature in degrees C.
  'slowCpm': n.n, # Counts per minute averaged from the last 22 seconds of data.
  'alarm': [True/False], # Ludlum 177 alarm output. Returns True when the Ludlum 177's alarm is going off.
  'baroPres': nnnnnn.n, # Barometric pressure in Pascals.
  'cpsGood': [True/False/Null], # Did we get at least 1 count in the last 22 seconds? If not something is probably wrong. Null means the fast CPM buffer isn't full.tsw@p80
  
  'cps': n, # Count of radiation detection events in the last second from the Ludlum 177.
  'baroTemp': nn.nn, # Barometer's temperature in degrees C.
  'fastCpm': n.n} # Counts per minute averaged from the last 4 seconds of data.
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