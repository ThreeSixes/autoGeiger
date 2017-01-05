<?php
// Make sure we're not loaded directly...

// Load our configuration.
require("config.php");

// RedisDB data layer.
class dlRedis {
    // Class-wide vars.
    
    // This will be our Redis object.
    private $rds = new Redis();
    
    // Constructor!
    function __construct() {
        $rds->connect(agConfig::config['redisHost'], agConfig::config['redisPort']);
    }
    
    // Get the last record in the cache.
    private function getLast() {
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