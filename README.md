#BEST HACK 2019. Guide по отборочному заданию от команды Going deeper


##Введение
Данная инструкция предназначается для программы, позволяющей узнать координаты точки сброса груза массой ***m***, разогнанного до скорости ***v*** на высоте ***h***, для попадания в точку с координатами (0, 0, 0) с разрешенной погрешностью с учетом аэродинамической силы, а также скорости ветров по оси **x** и **z**

##Запуск программы
Для запуска программы Вам понадобится:
1. Установленный интерпретатор **Python** версии **3.5** и выше
2. Установленные библиотеки **keras, numpy, pandas...**
3. Файлы:
 - **F.csv** с готовыми данными по зависимости аэродинамической силы от скорости груза
 - **Wind.csv** с информацией по скоростям ветра по осям x и z на высотах от 0 до 1400 метров

##Использование
По умолчанию директорией для поиска файлов **F.csv** и  **Wind.csv** будет являться директория размещения исполняемого кода. Если это подходит Вам, то ответьте **"Да"** на вопрос *"Использовать директорию по умолчанию?"*.
Если Вам необходимо использовать свою собственную директорию, где лежат необходимые файлы, то ответьте **"Нет"**. После программа предложит ввести абсолютный путь к вашей директории.
При некорректном ответе на любой из вопросов программа снова предложит вам ответить на него.
