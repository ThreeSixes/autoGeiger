<?php
// Make sure we're not loaded directly...

// Load our configuration.
require 'config.php';

// RedisDB data layer.
class dlRedis {
    // Class-wide vars.
    private $rds = null;
    private $cfg = null;
    
    // Constructor!
    function __construct() {
        global $rds;
        global $cfg;
        
        // Set up our Redis object.
        $rds = new Redis();
        $rds->connect("127.0.0.1", 6379);
    }
    
    // Get the last record in the cache.
    private function getLast() {
        global $rds;
        global $cfg;
        
        print_r($rds->get("autoGeigerLast"));
    }
    
    public function router($route) {
        switch($route[0]) {
            // Get the latest reading.
            case "latest":
                $this->getLast();
                break;
            
            default:
                break;
        }
        
    }
}
?>