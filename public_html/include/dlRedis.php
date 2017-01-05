<?php
// Make sure we're not loaded directly...

// Load our configuration.
require("config.php");

// RedisDB data layer.
class dlRedis {
    // Class-wide vars.
    private $rds = null;
    
    // Constructor!
    function __construct() {
        global $rds;
        
        try {
            echo agConfig::config['redisHost'];
            // Set up our Redis object.
            $rds = new Redis();
            $rds->connect(agConfig::config['redisHost'], agConfig::config['redisPort']);
        }
        
        catch(Exception $e) {
            echo "At __construct()::\n";
            echo $e->getMessage(); 
        }
    }
    
    // Get the last record in the cache.
    private function getLast() {
        global $rds;
        try {
            print($rds->get(agConfig::config['redisCacheName']));
        }
        
        catch(Exception $e) {
            echo "At getLast()::\n";
            echo $e->getMessage(); 
        } 
        
    }
    
    public function router($route) {
        switch($route[0]) {
            // Get the latest reading.
            case "latest":
                getLast();
                break;
        }
        
    }
}
?>