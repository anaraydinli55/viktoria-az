<?php

header("Content-Type: application/xml; charset=utf-8");

$colors = json_decode(file_get_contents("colors.json"), true);

$baseUrl = "https://www.viktoria-az.store/";
$imageBase = $baseUrl . "images/";

echo '<?xml version="1.0" encoding="UTF-8"?>';
echo '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">';
echo '<channel>';
echo '<title>Viktoria 10-QR Parça Boyaları</title>';
echo '<link>'.$baseUrl.'</link>';
echo '<description>62 rəngli avtomatik feed</description>';

foreach ($colors as $index => $c) {

echo '<item>';
echo '<g:id>V10QR-'.($index+1).'</g:id>';
echo '<title>Viktoria 10-QR – '.$c["color"].'</title>';
echo '<description>Qiymət: '.$c["price"].'</description>';
echo '<g:image_link>'.$imageBase.$c["file"].'</g:image_link>';
echo '<g:availability>in stock</g:availability>';
echo '<g:price>'.$c["price"].' AZN</g:price>';
echo '<g:brand>Viktoria</g:brand>';
echo '<g:condition>new</g:condition>';
echo '</item>';

}

echo '</channel>';
echo '</rss>';
?>
