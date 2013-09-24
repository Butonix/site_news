<?php 
     define('_SAPE_USER', '5557b1d2fcb87a21e41cb61718158ea1');
     require_once($_SERVER['DOCUMENT_ROOT'].'/'._SAPE_USER.'/sape.php'); 
     $sape_articles = new SAPE_articles();
     echo $sape_articles->process_request();
?>
