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
    
    // Try to ping the Redis server.
    private function ping() {
        global $rds;
        
        $pingRes = $rds->ping();
        print_r($pingRes);
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
            
            case "r":
                print("Made it... ");
                switch($route[1]) {
                    case "test":
                        print("Hit.");
                        $this->ping();
                        break;
                    
                    default:
                        break;
                }
                break;
            
            default:
                break;
        }
        
    }
}
?>