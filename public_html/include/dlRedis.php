<?php
// Make sure we're not loaded directly...

// RedisDB data layer.
class dlRedis {
    // Class-wide vars.
    // This will be our Redis object.
    private $rds = null;
    
    // Constructor!
    function __construct() {
        
    }
    
    // Get the last record in the cache.
    private function getLast() {
        return null;
    }
    
    public function router($route) {
        print("Hit Redis router.");
    }
}
?>