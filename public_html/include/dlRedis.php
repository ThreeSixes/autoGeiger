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
        
        $cfg = new agConfig();
        
        // Set up our Redis object.
        $rds = new Redis();
        $rds->connect(
            $cfg->config['redisHost'],
            $cfg->config['redisPort']
        );
    }
    
    // Get the last record in the cache.
    private function getLast() {
        global $rds;
        global $cfg;
        
        # Send data as JSON.
        header("Content-Type: application/json");
        print($rds->get($cfg->config['redisCacheName']));
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