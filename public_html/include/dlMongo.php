<?php
// Make sure we're not loaded directly...

// MongoDB data layer.
class dlMongo {
    // Class-wide vars.
    // This will be our mongoDB object.
    private $mdb = null;
    
    // Constructor!
    function __construct() {
        
    }
    
    // Get the last N records from the database.
    private function getLastN($numRecords) {
        return null;
    }
  
    // Route historical data requests.
    function router($req) {
        print("Hit Mongo router.");
    }
}
?>