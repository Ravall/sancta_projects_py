<?php
# определим регулярное выражение, которое будет парсить номера
define('PREG_PATTERN','/([78]?[\(\s]?\d{3}[\)\s]?\s?(?:\d[\-\s]?){6}\d{1})[\D?\Z]/');

function getPhonesFromText($text) 
{
    $array = array();
    preg_match_all(PREG_PATTERN, $text, $array);
    #выделим телефоны в чистом виде (без нецифр)
    $phones = array_map(
    	create_function(
    		'$rawPhone', 
    		'return preg_replace(
    					array("/\D/", "/^7/", "/^495/"), 
    					array("", "8", "8495"),
    					$rawPhone
    				);'
    	), $array[1]
    );
    return $phones;
}



# для тестов
$testString = 'мой телефон 79265380140 (89265380240)
или по другому 8(926)3335588
другие записи
8-926-53-800-41
7 926 53 800 42
7 926 538-00-43
8(926) 538 00 44

8(926) 538 00 45

мой прямой номер 495 664-44-60 и 8(495) 664-44-61';

getPhonesFromText($testString);