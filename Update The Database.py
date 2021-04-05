# Здравствуйте, В данном коде я попытался подробно описать каждое действие, надеюсь, что у меня это получилось :)

# Импортируем библиотеку для работы с URL
import requests
# А ещё импортируем библиотеку для работы с командной строкой в Windows (У меня 10)
import os

# Создаём строку, которая будет содержать в себе текст HTML файла с сайта,
# на котором размещена таблица со 100 игроками
Main_string = requests.get('https://www.gokgs.com/top100.jsp').text

# Дальше мы будем использовать текстовый файл для "общения" с JS-кодом
File_FOR_JS = open('Data_Base.txt', 'w', encoding='UTF-8')

# Данный цикл будет выполняться 100 раз, так как мы должны собрать информацию про всех участников таблицы
for i in range(100):

    # Создаём простые массивы, которые будут содержать ссылки на две наши последние партии, на два типа и счёта партии
    
    # 0 - Ссылка на последнюю партию игрока
    # 1 - Тип партии последней игры
    part_last = [0] * 2

    # 0 - Ссылка на предпоследнюю партию игрока
    # 1 - Тип партии предпоследней игры
    part_penultimate = [0] * 2

    # Данная группа операций находит нам ИМЯ игрока в строке, содержащей в себе таблицу 100 игроков
    # После чего "сокращает" своё содержимое. Можно сказать, что она худеет для немного большей производительности кода
    Main_string.find('graph')
    Main_string = Main_string[Main_string.find('graph') : ]
    Main_string = Main_string[Main_string.find('>') + 1 : ]
    Name = Main_string[0:Main_string.find('<')] # Строка, которая хранит в себе имя игрока

    print(Name)
    if Name == 'Tolstoi':
        print(Name)
        continue

    # В данной строке находится HTML файл со страници, на которой находится информация про отдельноо игрока
    Secondary_string = requests.get('https://www.gokgs.com/gameArchives.jsp?user=' + Name).text
    Secondary_string = Secondary_string[Secondary_string.find('(') + 1 : ] # Немнго укорациваем нашу строку(делаем меньше)
    
    # Создаём резервную/запасную строку, которая нам мажет понадобится, если игрок сыграл только одну игру за весь месяц
    Reserve_string = Secondary_string
    brace = Secondary_string[ : Secondary_string.find('g') - 1] # В данной строке содержится количество партий игрока за месяц

    # Инициализируем необходимы максимальные значения года и месяца игры,
    # в далнейшем мы будем от них отталкиваться при поиске партий игрока
    year = 2021
    month = 12

    # Особенность сайта в том, что если игрок сыграл хоть одну партию в нашем месяце на данный момент
    # (на момент написания кода - Март), то она отображается сразу при запуске страницы и ссылка на последнем месяце
    # уже не работает. В ином случае не выводится ничего, но ссылка на последний месяц доступна
    # В данном условии проверяется такая ситуация
    if brace == '0':
        Party_string = Secondary_string
    else:

        # В данном цыкле мы ищем последий год, в котором была сыграна последняя партия
        # Например, если у игрока нет игр за весь 2021 год, то мы ищем игры за 2020 год и так далее
        while Secondary_string.find('<td>' + str(year) + '</td>') == -1:
            year = year - 1

        # Сокращаем содержимое строки
        Secondary_string = Secondary_string[Secondary_string.find('<td>' + str(year) + '</td>') : ]

        # В данном цыкле мы ищем последий месяц, в котором была сыграна последняя партия
        # Например, если у игрока нет игр за весь Декабрь(12 месяц), то мы ищем игры за Ноябрь(11 месяц) и так далее
        while Secondary_string.find('month=' + str(month)) == -1:
            if month == -1:
                month = 12
                break
            month = month - 1

        # Мы нашли месяц и год последней партии, пора открыть страницу с таблицей игр данного игрока
        Party_string = requests.get('https://www.gokgs.com/gameArchives.jsp?user=' + Name +  '&year=' + str(year) + '&month=' + str(month)).text
        Party_string = Party_string[Party_string.find('(') + 1 : ]
        brace = Party_string[ : Party_string.find('g') - 1] # Здесь мы ищем количество партий за данный месяц

        # Бывают такие ситуации, когда за меся угрок сыграл только олну партию. 
        # И в таком случае невозможно получить ссылку на вторую партию. Данное условие проверяет такую ситуацию
    
    if brace == '1':
        
        while Party_string.find('href="h') == -1:
            if month == 1:
                year = year - 1
                month = 12
            else:
                month = month - 1
            Party_string = requests.get('https://www.gokgs.com/gameArchives.jsp?user=' + Name +  '&year=' + str(year) + '&month=' + str(month)).text
            Party_string = Party_string[Party_string.find('(') + 1 : ]
            brace = Party_string[ : Party_string.find('g') - 1]

        # Данную единственную партию записываем в наш массив партий, т.к. она и вправду самая последняя
        Party_string = Party_string[Party_string.find('href="h') + 6 : ]
        part_last[0] = Party_string[ : Party_string.find('"')]
        Party_string = Party_string[Party_string.find('"') : ]

        # Здесь мы заполныем полу массива, которое отвечает за тип партии
        if Party_string.find('Ranked') != -1:
            part_last[1] = 'Ранговая'
        elif Party_string.find('Free') != -1:
            part_last[1] = 'Свободная'
        else:
            part_last[1] = ' nope '

        # А предпоследнюю партию нужно искать в прошлом месяце. А если месяц уже Декабрь, то и в прошлом году, начиная с Января
        # Именно здесь нам и понадобится резервная строка
        
        # Данная часть кода будет явно касаться игрока tetsujin, он мне очен помог в составлении данного кода
        # (на мамент написания кода он находился на 10 месте и имел только одну партию за Март 2021 года)
        
        # Если у нас Декабрь, то мы откатываемся назад на год и берём Январь
        if month == 1:
            year = year - 1
            month = 12
        else:
            month = month - 1
        
        # Цикл, который проверяет есть ли ссылки на данынй месяц данного года
        while Reserve_string.find('year=' + str(year) + '&amp;month=' + str(month)) == -1:
            if month == 1:
                year = year - 1
                month = 12
            else:
                month = month - 1

        # Когда мы нашли новый месяц и год, то получаем HTML этого нового игрового месяца нашего игрока
        Reserve_string = requests.get('https://www.gokgs.com/gameArchives.jsp?user=' + Name +  '&year=' + str(year) + '&month=' + str(month)).text
        Reserve_string = Reserve_string[Reserve_string.find('(') + 1: ]

        # Это переменная, которая будет хранить количество партий на данный месяц
        brace_Reserve = Reserve_string[ : Reserve_string.find('g') - 1]

        # Цикл, который проверяет, есть ли игры у игрока на данный месяц 
        while brace_Reserve == '0':
            if month == 1:
                year = year - 1
                month = 12
            else:
                month = month - 1
            Reserve_string = requests.get('https://www.gokgs.com/gameArchives.jsp?user=' + Name +  '&year=' + str(year) + '&month=' + str(month)).text
            Reserve_string = Reserve_string[Reserve_string.find('(') + 1: ]
            brace_Reserve = Reserve_string[ : Reserve_string.find('g') - 1]
        
        # Как только мы нашли месяц, в который игрок играл, то ищем первую партию и записываем её во второе поле массива партий
        Reserve_string = Reserve_string[Reserve_string.find('href="h') + 6 : ]
        part_penultimate[0] = Reserve_string[ : Reserve_string.find('"')]

        # Здесь мы заполныем полу массива, которое отвечает за тип партии
        if Party_string.find('Ranked') != -1:
            part_penultimate[1] = 'Ранговая'
        elif Party_string.find('Free') != -1:
            part_penultimate[1] = 'Свободная'
        else:
            part_penultimate[1] = ' nope '

        #
        # Это была самая сложная часть кода, так что дальше будет легче и понятнее :)
        #

    # Если за месяц игрок совершил больше одной игры, то сразу всё становится легче!
    else:

        while Party_string.find('href="h') == -1:
            if month == 1:
                year = year - 1
                month = 12
            else:
                month = month - 1
            Party_string = requests.get('https://www.gokgs.com/gameArchives.jsp?user=' + Name +  '&year=' + str(year) + '&month=' + str(month)).text
            Party_string = Party_string[Party_string.find('(') + 1 : ]
            brace = Party_string[ : Party_string.find('g') - 1]
        # Мы просто записываем две последние игры в два поля массива партий
        # 1
        Party_string = Party_string[Party_string.find('href="h') + 6 : ]
        part_last[0] = Party_string[ : Party_string.find('"')]

        # Здесь мы заполныем полу массива, которое отвечает за тип партии
        if Party_string.find('Ranked') != -1:
            part_last[1] = 'Ранговая'
        elif Party_string.find('Free') != -1:
            part_last[1] = 'Свободная'
        else:
            part_last[1] = ' nope '

        while Party_string.find('href="h') == -1:
            if month == 1:
                year = year - 1
                month = 12
            else:
                month = month - 1
            Party_string = requests.get('https://www.gokgs.com/gameArchives.jsp?user=' + Name +  '&year=' + str(year) + '&month=' + str(month)).text
            Party_string = Party_string[Party_string.find('(') + 1 : ]
            brace = Party_string[ : Party_string.find('g') - 1]
        # 2
        Party_string = Party_string[Party_string.find('href="h') + 6 : ]
        part_penultimate[0] = Party_string[ : Party_string.find('"')]

        # Здесь мы заполныем полу массива, которое отвечает за тип партии
        if Party_string.find('Ranked') != -1:
            part_penultimate[1] = 'Ранговая'
        elif Party_string.find('Free') != -1:
            part_penultimate[1] = 'Свободная'
        else:
            part_penultimate[1] = ' nope '

    Sgf_string = requests.get(part_last[0]).text # Здесь мы скачиваем SGF-файл с игрой
    
    File_FOR_JS.write(Name + '\n')
    File_FOR_JS.write('PARTY' + '\n')

    Sgf_string = Sgf_string[Sgf_string.find('PW') : ]

    # Для начала найдём и напечатаем имена и цвет камней наших участников
    # Белые камни - имя
    File_FOR_JS.write('Белые ' + Sgf_string[3 : Sgf_string.find(']')] + '\n')
    # Черные камни - имя
    Sgf_string = Sgf_string[Sgf_string.find('PB') : ]
    File_FOR_JS.write('Чёрные ' + Sgf_string[3 : Sgf_string.find(']')] + '\n')

    # Здесь мы сокращаем строку, чтобы "опции партии" нам не мешали в далнейшем, мы и так всё уже знаем
    Sgf_string = Sgf_string[Sgf_string.find('RE') : ]

    # Пора записат тип партии. Ранговая или свободная
    File_FOR_JS.write(part_last[1] + ' ')
    # А также нельзя забыват про результат партии
    File_FOR_JS.write(Sgf_string[3 : Sgf_string.find(']')] + '\n')

    # И немного укорачиваем строку
    Sgf_string = Sgf_string[Sgf_string.find(';') : ]

    # В этой переменной у нас будет храниться время. К этому мы ещё вернёмся
    time_FLOAT = 0
    
    # Иии ... Создаём цикл, который будет проходит по кадома значению SGF-файла, будь то число или буква
    while Sgf_string.find('B') != -1 or Sgf_string.find('W') != -1:
        
        # Здес мы убираем знак ";", так как нам нужно будет найти такой же знак, но только на следующей строке, чтобы сократить строку
        Sgf_string = Sgf_string[1 : ]
        
        # Записываем в SGF-файл очерёдность хода и пересечение на доске
        # Очерёдность
        File_FOR_JS.write(Sgf_string[ : Sgf_string.find('[')])
        # Координаты
        File_FOR_JS.write(Sgf_string[Sgf_string.find('[') + 1 : Sgf_string.find(']')] + '.')
        
        # Готовим строку к поиску значения времени, за которое был совершён ход
        Sgf_string = Sgf_string[Sgf_string.find(']') + 1 : ]
        
        # Когда строка уже готова, извлекаем из неё число с точкой(и без точки) и,конвертировав в float, записываем его в переменную
        if Sgf_string[Sgf_string.find('L') + 2 : Sgf_string.find(']')] ==  '':
            break

        if Sgf_string.find('L') != -1:
            time_FLOAT = time_FLOAT + float(Sgf_string[Sgf_string.find('L') + 2 : Sgf_string.find(']')])
        
        # Сокращаем строку на строку, именно здес мы и используем ";" 
        Sgf_string = Sgf_string[Sgf_string.find(';') : ]

    # Осталось толко записат время всей партии
    File_FOR_JS.write('\n' + 'Время ' + str(time_FLOAT))

    #
    #
    File_FOR_JS.write('\n' + 'PARTY' + '\n')
    #
    #

    Sgf_string = requests.get(part_penultimate[0]).text # Здесь мы скачиваем SGF-файл уже с предпоследней игрой
    
    # Для начала найдём и напечатаем имена и цвет камней наших участников
    # Белые камни - имя
    Sgf_string = Sgf_string[Sgf_string.find('PW') : ]
    File_FOR_JS.write('Белые ' + Sgf_string[3 : Sgf_string.find(']')] + '\n')
    # Черные камни - имя
    Sgf_string = Sgf_string[Sgf_string.find('PB') : ]
    File_FOR_JS.write('Черные ' + Sgf_string[3 : Sgf_string.find(']')] + '\n')

    # Здесь мы сокращаем строку, чтобы "опции партии" нам не мешали в далнейшем, мы и так всё уже знаем
    Sgf_string = Sgf_string[Sgf_string.find('RE') : ]

    # Пора записат тип партии. Ранговая или свободная
    File_FOR_JS.write(part_last[1] + ' ')
    # А также нельзя забыват про результат партии
    File_FOR_JS.write(Sgf_string[3 : Sgf_string.find(']')] + '\n')

    # И немного укорачиваем строку
    Sgf_string = Sgf_string[Sgf_string.find(';') : ]

    # В этой переменной у нас будет храниться время. К этому мы ещё вернёмся
    time_FLOAT = 0
    
    # Иии ... Создаём цикл, который будет проходит по кадома значению SGF-файла, будь то число или буква
    while Sgf_string.find('B') != -1 or Sgf_string.find('W') != -1:
        
        # Здес мы убираем знак ";", так как нам нужно будет найти такой же знак, но только на следующей строке, чтобы сократить строку
        Sgf_string = Sgf_string[1 : ]
        
        # Записываем в SGF-файл очерёдность хода и пересечение на доске
        # Очерёдность
        File_FOR_JS.write(Sgf_string[ : Sgf_string.find('[')])
        # Координаты
        File_FOR_JS.write(Sgf_string[Sgf_string.find('[') + 1 : Sgf_string.find(']')] + '.')
        
        # Готовим строку к поиску значения времени, за которое был совершён ход
        Sgf_string = Sgf_string[Sgf_string.find(']') + 1 : ]
        
        if Sgf_string[Sgf_string.find('L') + 2 : Sgf_string.find(']')] ==  '':
            break

        if Sgf_string.find('L') != -1:
        # Когда строка уже готова, извлекаем из неё число с точкой(и без точки) и,конвертировав в float, записываем его в переменную
            time_FLOAT = time_FLOAT + float(Sgf_string[Sgf_string.find('L') + 2 : Sgf_string.find(']')])
        
        # Сокращаем строку на строку, именно здес мы и используем ";" 
        Sgf_string = Sgf_string[Sgf_string.find(';') : ]

    # Осталось толко записат время всей партии
    File_FOR_JS.write('\n' + 'Время ' + str(time_FLOAT))

    #
    #
    File_FOR_JS.write('\n' + 'END' + '\n')
    #
    #  

# И не забыть закрыть файлик
File_FOR_JS.close() 


# ВОТ И КОДУ КОНЕЦ! 
# Прошу перейти в JS-файл для дальнейшего ознакомления с проектом