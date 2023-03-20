<?php

require_once('functions.php');

if(isset($_POST['username']) && isset($_POST['password'])){
    list($username, $password) = [$_POST['username'], $_POST['password']];

    if(login($username, $password)){
        $_SESSION['username'] = $username;
        header('Location: admin.php');
    }else{
        flash('Wrong username or password');
    }
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
    <form method="POST">
        <div class="container">
        <div class="columns">
  <div class="column is-one-third">
  <div class="field">
                <label class="label">Username</label>
                <div class="control">
                    <input class="input" type="text" placeholder="Username" name="username">
                </div>
            </div>

            <div class="field">
              <label class="label">Password</label>
              <div class="control">
                <input class="input" type="password" placeholder="Password" name="password">
              </div>
              <?php
              $flash = get_flash_msg();
              if($flash){
                echo "<p class=\"help is-danger\">$flash</p>";
              }
              
              ?>
            </div>

            <div class="control">
                <button class="button" type="submit">Login</button>
            </div>
        </div>
  </div>
</div>
           
        </form>
    </div>
  </div>
</div>

    

    </body>
</html>