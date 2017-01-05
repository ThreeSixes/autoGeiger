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
        
        $retVal = array("Content-Type: application/json", "{}");
        
        // Try to ping.
        if ($rds->ping() == "+PONG") {
            $retVal[1] = '{"alive": true}';
        } else {
            $retVal[1] = '{"alive": false}';
        }
    }
    
    // Get the last record in the cache.
    private function getLast() {
        global $rds;
        global $cfg;
        
        # Return all the things.
        return array("Content-Type: application/json", $rds->get($cfg->config['redisCacheName']));
    }
    
    public function router($route) {
        # Return value for headers and data.
        $retVal = array(null, null);
        
        switch($route[0]) {
            // Get the latest reading.
            case "latest":
                $retVal = $this->getLast();
                break;
            
            case "r":
                switch($route[1]) {
                    case "test":
                        $retVal = $this->ping();
                        break;
                    
                    default:
                        break;
                }
                break;
            
            default:
                break;
        }
        
        return $retVal;
    }
}
?>