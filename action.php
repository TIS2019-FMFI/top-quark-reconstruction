<?php
echo "Parameters were written into config file successfully";
 $path = 'config.txt';
 file_put_contents("config.txt", "");
 if (isset($_POST['p1']) && isset($_POST['p2']) && isset($_POST['p3'])&& isset($_POST['p4'])&& isset($_POST['p5'])&& isset($_POST['p6'])&& isset($_POST['p7']) && isset($_POST['p8'])
 && isset($_POST['p9']) && isset($_POST['p10']) && isset($_POST['p11'])&& isset($_POST['p12'])&& isset($_POST['p13'])&& isset($_POST['p14'])&& isset($_POST['p15'])
  && isset($_POST['p16'])&& isset($_POST['p17'])&& isset($_POST['p18'])&& isset($_POST['p19'])&& isset($_POST['p20'])) {
    $fh = fopen($path,"a+");
    $string = 'filename = '.$_POST['p1'].PHP_EOL;


    $string2 = 'path = '.$_POST['p2'].PHP_EOL;
    $string3 = 'batch_size = '.$_POST['p3'].PHP_EOL;
    $string4 = 'alpha = '.$_POST['p4'].PHP_EOL;
    $string5 = 'iteration = '.$_POST['p5'].PHP_EOL;
    $string6 = 'path_to_save = '.$_POST['p6'].PHP_EOL;
    $string7 = 'saved_as = '.$_POST['p7'].PHP_EOL;
    $string8 = 'minimum = '.$_POST['p8'].PHP_EOL;
    $string9 = 'maximum = '.$_POST['p9'].PHP_EOL;
    $string10 = 'run_minmax = '.$_POST['p10'].PHP_EOL;

    $string11 = 'loss = '.$_POST['p11'].PHP_EOL;
    $string12 = 'metrics = '.$_POST['p12'].PHP_EOL;
    $string13 = 'monitor = '.$_POST['p13'].PHP_EOL;
    $string14 = 'mode = '.$_POST['p14'].PHP_EOL;
    $string15 = ''.$_POST['p15'].PHP_EOL;
    $string16 = ''.$_POST['p16'].PHP_EOL;
    $string17 = ''.$_POST['p17'].PHP_EOL;
    $string18 = ''.$_POST['p18'].PHP_EOL;
    $string19 = ''.$_POST['p19'].PHP_EOL;
    $string20 = ''.$_POST['p20'];








    fwrite($fh,$string); // Write information to the file

    fwrite($fh,$string2); // Write information to the file
    fwrite($fh,$string3); // Write information to the file
    fwrite($fh,$string4); // Write information to the file
    fwrite($fh,$string5); // Write information to the file
    fwrite($fh,$string6); // Write information to the file
    fwrite($fh,$string7); // Write information to the file
    fwrite($fh,$string8); // Write information to the file
    fwrite($fh,$string9); // Write information to the file
    fwrite($fh,$string10); // Write information to the file

    fwrite($fh,$string11); // Write information to the file
    fwrite($fh,$string12); // Write information to the file
    fwrite($fh,$string13); // Write information to the file
    fwrite($fh,$string14); // Write information to the file
    fwrite($fh,$string15); // Write information to the file
    fwrite($fh,$string16); // Write information to the file
    fwrite($fh,$string17); // Write information to the file
    fwrite($fh,$string18); // Write information to the file
    fwrite($fh,$string19); // Write information to the file
    fwrite($fh,$string20); // Write information to the file
    fclose($fh); // Close the file
 }
?>
