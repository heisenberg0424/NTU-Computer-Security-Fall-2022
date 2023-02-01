<?php
  if(isset($_FILES['file'])){
    $file = $_FILES['file'];

    if( preg_match('/ph/i', $file['name']) !== 0
     || preg_match('/ph/i', file_get_contents($file['tmp_name'])) !== 0
     || $file['size'] > 0x100
    ){ die("Bad file!"); }
    
    $uploadpath = 'upload/'.md5_file($file['tmp_name']).'/';
    @mkdir($uploadpath);
    move_uploaded_file($file['tmp_name'], $uploadpath.$file['name']);

    Header("Location: ".$uploadpath.$file['name']);
    die("Upload success!");
  }
  highlight_file(__FILE__);
?>

<form method=POST enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>

