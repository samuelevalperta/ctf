<?php

require_once('functions.php');

// if the user is not logged, go back to the login
if(!check_auth('admin')){
    flash('You need to sign in to do that.');
    header('Location: login.php');
}

if(isset($_GET['logout'])){
    unset($_SESSION['username']);

    flash('Logged out');
    header('Location: login.php');
}

?>

<!DOCTYPE html>
<html>
    <head>
        <title>Login</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
        <link rel="stylesheet" href="https://unpkg.com/bulmaswatch/superhero/bulmaswatch.min.css">
    <style>
.hero.has-background {
  position: relative;
  overflow: hidden;
}
.hero-background {
  position: absolute;
  object-fit: cover;
  object-position: center center;
  width: 100%;
  height: 100%;
}
.hero-background.is-transparent {
  opacity: 0.3;
}
    </style>
      </head>
    <body class="has-background">
    <nav class="navbar is-fixed-top  is-transparent" role="navigation" aria-label="main navigation">
  
    <div class="navbar-menu">
    <div class="navbar-start">
      <a class="navbar-item" href="/">
        Home
      </a>

      <a class="navbar-item" href="/login.php">
        Login
      </a>
    </div>
    </div>
    </nav>
    
    <div class="hero is-fullheight has-background">
  <img  class="hero-background is-transparent" src="https://upload.wikimedia.org/wikipedia/commons/1/11/Galactic_Cntr_full_cropped.jpg" />
  <div class="hero-body">
    <div class="container">
      <h1 class="title">
      This should be some kind of admin portal. My fantasy has reached an end manking.
      </h1>
      <h3 class="subtitle">
      Btw (I use arch) here is the flag: <?= FLAG ?>
      </h3>
    </div>
  </div>
</div>

    </body>
</html>
