<?php
echo "Parameters were written into config file successfully";
 $path = 'config.txt';
 file_put_contents("config.txt", "");
 if (isset($_POST['p1']) && isset($_POST['p2']) && isset($_POST['p3'])&& isset($_POST['p4'])&& isset($_POST['p5'])&& isset($_POST['p6'])&& isset($_POST['p7'])) {
    $fh = fopen($path,"a+");
    $string = 'filename = '.$_POST['p1'].PHP_EOL;


    $string2 = 'path = '.$_POST['p2'].PHP_EOL;
    $string3 = 'batch_size = '.$_POST['p3'].PHP_EOL;
    $string4 = 'alpha = '.$_POST['p4'].PHP_EOL;
    $string5 = 'iteration = '.$_POST['p5'].PHP_EOL;
    $string6 = 'path_to_save = '.$_POST['p6'].PHP_EOL;
    $string7 = 'saved_as = '.$_POST['p7'];
    fwrite($fh,$string); // Write information to the file

    fwrite($fh,$string2); // Write information to the file
    fwrite($fh,$string3); // Write information to the file
    fwrite($fh,$string4); // Write information to the file
    fwrite($fh,$string5); // Write information to the file
    fwrite($fh,$string6); // Write information to the file
    fwrite($fh,$string7); // Write information to the file
    fclose($fh); // Close the file
 }
?>
