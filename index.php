<!DOCTYPE html>
<?php


if(isset($_POST['submit'])){
  $user = $_POST['username'];
  $password = $_POST['password'];
  $pass = md5($_POST['password']);

  $filename = "md5.txt";
  $handler = fopen($filename,"r");
  $filepass=fread($handler,filesize($filename));
  if($user == 'kvarky' and $pass == $filepass){

  echo "<script> window.location.assign('second.html'); </script>";


  }
  else{
    echo "wrong password";
  }
}



?>
<html>
<head>
<title>Top quark recontruction</title>
<meta charset="UTF-8">
<link rel="stylesheet" type="text/css" href="stylesheet.css">
</head>
<center><body class = "main">

  <form id="prihlasenie"  method="post">
  	<fieldset>
  		<h3>LOG IN</h3>
  		<label for="username">Username:</label>
  		<input name="username" type="text" id="username" value="" size="20" maxlength="50" required>
  		<br>
  		<label for="password">Password: </label>
  		<input name="password" type="password" id="password" size="20" maxlength="15" value ="" required>
  		<br>
  	</fieldset>
  	<p><input name="submit" type="submit" id="submit" value="Login"> <input type="reset">
  	</p>
  </form>

</body>

</html>
