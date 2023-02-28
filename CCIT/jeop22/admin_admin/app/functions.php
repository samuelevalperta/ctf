<?php

// Start the session
session_start();

// set some constants

define('FLAG', getenv('FLAG'));
define('ADMIN_PWD_HASH', getenv('ADMIN_PWD_HASH'));

function check_auth($for_user){
    return isset($_SESSION['username']) ? $_SESSION['username'] == $for_user: FALSE;
}

function login($username, $password){
    if($username == 'admin'){
        return password_verify($password, ADMIN_PWD_HASH);
    }
    return FALSE;
}

function flash($message){
    $_SESSION['flash'] = $message;
}

function get_flash_msg(){
    $msg = isset($_SESSION['flash'])? $_SESSION['flash']: '';
    $_SESSION['flash'] = '';
    return $msg;
}