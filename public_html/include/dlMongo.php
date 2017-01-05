<?php
// Make sure we're not loaded directly...

// Load our configuration.
require 'config.php';

// MongoDB data layer.
class dlMongo {
    // Class-wide vars.
    // This will be our mongoDB object.
    //private $mdb = null;
    
    // Constructor!
    public function __construct() {
        
    }
    
    // Get the last N records from the database.
    private function getLastN($numRecords) {
        return null;
    }
  
    // Route historical data requests.
    function router($route) {
        return array(null, null);
    }
}
?>