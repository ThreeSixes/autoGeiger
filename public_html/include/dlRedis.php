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
        
        // Set up our Redis object.
        $rds = new Redis();
        $rds->connect(agConfig::config['redisHost'], agConfig::config['redisPort']);
    }
    
    // Get the last record in the cache.
    private function getLast() {
        global $rds;
        print($rds->get(agConfig::config['redisCacheName']));
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