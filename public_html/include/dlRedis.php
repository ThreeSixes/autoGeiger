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
        
        try {
            echo $cfg->config['redisHost'];
            // Set up our Redis object.
            $rds = new Redis();
            $rds->connect($cfg->config['redisHost'], $cfg->config['redisPort']);
        }
        
        catch(Exception $e) {
            print("At __construct()::\n");
            print($e->getMessage()); 
        }
    }
    
    // Get the last record in the cache.
    private function getLast() {
        global $rds;
        global $cfg;
        
        try {
            print($rds->get($cfg->config['redisCacheName']));
        }
        
        catch(Exception $e) {
            print("At getLast()::\n");
            print($e->getMessage()); 
        } 
        
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