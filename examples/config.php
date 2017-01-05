<?php
// This should be copied to /opt/autoGeiger/public_html/include/

// Don't allow this to be loaded directly 'cuz security.
if (!defined('LOADFROMAPI')) die("ZOMGSKIDDIEZ!");

// Just for giggles wrap this in a class?
class agConfig {
    // Define settings for this instance.
    public function config() {
        return array(
        # Redis settings
        "redisHost" => "127.0.0.1",
        "redisPort" => 6379,
        "redisCacheName" => "autoGeigerLast",
        
        # MongoDB settings.
        "mongoHost" => "127.0.0.1",
        "mongoPort" => 27017,
        "mongoDb" => "autoGeiger",
        "mongoColl" => "samples"
    );
    }
}
?>