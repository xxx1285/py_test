<?php

//Название класса таблицы товаров в БД
$cf_config['className'] = 'MyaghCo';
//Название пакета таблицы товаров в БД
$cf_config['packageName'] = 'myagh';
//Название поля ID родителя
$cf_config['parent_field'] = 'resource_id';

//разбивка по столбцам при импорте и экспорте (content|tv|category)
$cf_config['content_row'] = array(
    array('name_tovar_ua',array('pagetitle','content')),
    array('kod_tovar',array('articul','content')),
    array('brend',array('brend','content')),
    array('price',array('price','content')),
    array('dlina',array('razmerd','content')),
    array('glubina',array('razmerg','content')),
    array('visota',array('razmerv','content')),
    array('spalnoe',array('razmersp','content')),
    array('image',array('image','content')),
    array('mimage1',array('mimage1','content')),
    array('mimage2',array('mimage2','content')),
    array('mimage3',array('mimage3','content')),
    array('mimage4',array('mimage4','content')),
    array('mimage5',array('mimage5','content')),
    array('mimage6',array('mimage6','content')),
    array('mimage7',array('mimage7','content')),
    array('mimage8',array('mimage8','content')),
    array('mimage9',array('mimage9','content')),
    array('mimage10',array('mimage10','content')),
    array('mimage11',array('mimage11','content')),
    array('mimage12',array('mimage12','content')),
    array('mimage13',array('mimage13','content')),
    array('mimage14',array('mimage14','content')),
    array('mimage15',array('mimage15','content')),
    array('mimage16',array('mimage16','content')),
    array('mimage17',array('mimage17','content')),
    array('mimage18',array('mimage18','content')),
    array('mimage19',array('mimage19','content')),
    array('mimage20',array('mimage20','content'))
);
//значения по умолчанию при импорте или проверка при экспорте
$cf_config['imp_content_default'] = array(
    'content' => array(
        'deleted' => 0,
        'published' => 1,
        //'createdon' => strtotime("now"),
        //'publishedon' => strtotime("now"),
        //'editedby' => 1,
        //'editedon' => strtotime("now")
    ),
    'tv' => array(
        //7 => 0
    )
);

//первая строка - названия полей
$cf_config['include_captions'] = true;

//число товаров импортируемых за один раз (загрузка по группам). 0 - не ограничивать.
$cf_config['batch_import'] = 0;

//разбивать по категориям
$cf_config['include_categories'] = false;

//удалять дочерние категории при очистке и обновлении каталога
$cf_config['delete_subcategories'] = false;

//по какому полю проверять соответствие товара при обновлении. false - не проверять (очистка категории при обновлении).
$cf_config['imp_chk_field'] = 'articul';

//проверять соответствие товара при обновлении по значению TV. Указать ID TV. false - не проверять (очистка категории при обновлении).
$cf_config['imp_chk_tvid_val'] = false;

//Добавлять товары, которые не найдены при обновлении по TV (imp_chk_tvid_val) или полю (imp_chk_field)
$cf_config['imp_if_not_exist'] = true;

//удалять HTML-теги при экспорте
$cf_config['exp_strip_tags'] = false;

//автоматически генерировать псевдоним (alias) при импорте
//false - выключено; true - генерировать с переводом в транслит; 'notranslit' - генерировать без перевода в транслит.
$cf_config['imp_autoalias'] = true;

//Изменить значения поля для всех вложенных товаров до начала импорта.
//Например можно отменить публикацию для всех товаров и публиковать только те, которые есть в новом прайс-листе.
//первый массив - какие поля и на какие значения менять, второй массив - условия которые нужно проверять (можно сделать пустым)
$cf_config['imp_before_change'] = false;//'[{"tv.inventory":0},{}]';//'[{"published":0},{"tv.pricename":"Поставщик1"}]';//false - для отмены

//удалить файл после экспорта (скачивания)
$cf_config['exp_delete_file'] = false;

//кодировка CSV-файла при экспорте
$cf_config['exp_csv_charset'] = 'UTF-8'; //'UTF-8'; 'windows-1251'

//Импортировать (обновлять) пустые значения
$cf_config['imp_empty'] = true;

//Имя файла процессора, который использовать для импорта. Если пусто, используется стандартный процессор "import".
$cf_config['imp_custom_processor'] = '';

//путь (xpath) в XML структуре до товаров
$cf_config['imp_xml_itemsparent_path'] = '';//'/catalog/shop/offers';

//Структура XML файла для импорта
$cf_config['imp_xml_structure'] = <<<EOF
<Good>
    <Articul>articul</Articul>
    <Name>pagetitle</Name>
    <Price>price</Price>
</Good>
EOF;

//тестирование конфигурации (без записи в БД). Отчёты -> Журнал ошибок.
$cf_config['imp_testmode'] = false;

//функция для фильтрации значений при ИМПОРТЕ
function filter_import($value_arr){
    $output_arr = $value_arr;
    /*
    if(isset($output_arr['content']['pagetitle']))
        $output_arr['content']['pagetitle'] = mb_strtoupper($output_arr['content']['pagetitle'], 'UTF-8');
    */
    return $output_arr;
}


//функция для фильтрации значений при ЭКСПОРТЕ
function filter_export($value_arr,$doc_id=0){
    $output_arr = $value_arr;
    //var_dump($value_arr,$output_arr);
    //exit;
    /*
    if(isset($output_arr['price']))
        $output_arr[1] = floatval($output_arr[1]) - 200;
    */
    return $output_arr;
}


?>
