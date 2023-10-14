welcome_message: str = '''
Я категорически вас приветствую! Данный бот предназначен для конвертирования видео из Ютуба в аудио файл, а также отпраки несмешных анекдотов. 
Отправьте боту ссылку на интересующее вас видео, а бот отправит аудио файлы со звуковой дорожкой
'''

commands_dict: dict[str: str] = {
    'help': '''Для того, чтобы получить аудио файл нужного видео, необходимо скопировать ссылку на видео и отправить её боту(пример подобной ссылки: https://www.youtube.com/watch?v=dQw4w9WgXcQ)
ВАЖНЫЕ УТОЧНЕНИЯ!
1) Бот делит аудио на части[id_номер] по 45 минут. Это сделано, чтобы обойти ограничения telegram без потерь качества звука
2) Аудио файлы хранятся в расширении opus
3) Бот не способен обрабатывать прямые трансляции
4) Если есть замечания или предложения по улучшению бота, то можете написать мне в личку: @Tokin_Nikita''',
    'GitHub_Directory': 'Директория кода - https://github.com/Jadedboat780/Podcast_Bot.git'
}

base_anecdote: dict[int: str] = {
    1: 'Едут по пустыни два армянина инвалида-колясочника. Тут один из них находит лампу, начинает тереть. Вылез джин и говорит:\n-У вас одно желание на двоих.\nОни думали, думали, и в один голос сказали:\n-Мы хотим ходить.\nА джин им говорит:\n-Так как желание одно на двоих, ходить будете по очереди.\nИ дал им нарды',
    2: 'Французский турист в Израиле хочет совершить поездку на прогулочном катере по Тивериадскому озеру. Владелец катера называет ему цену, тот быстро переводит в уме и произносит:\n- Пятьсот евро! Вы что, обалдели!?\n- Но, месье, на этом озере сам Иисус прошёл пешком по воде.\n- Немудрено, с вашими-то тарифами...',
    3: 'Осел спрашивает у льва:\n-Почему ты король саванны, а не я?\nЛев отвечает:\n-Осел, ты в саванне не живешь.\n-А, точно - отвечает осел и исчезает',
    4: 'В интернете был проведен опрос: "Чей Крым?"\n100% опрошенных ответили "НАШ!',
    5: 'Сидят Василий Иванович с Петькой, тут Петька орет:\n– Василий Иванович, белые идут!\nТут Василий Иванович подорвался, ну, и бежать. Петька говорит:\n– Василий Иванович, не хорошо получается, выходит, отступаем?\nВасилий Иванович:\n– Дурак ты, Петька, земля круглая – с тыла заходим!',
    6: 'Как называется съезд врачей альтернативной медицины?\n.\n.\n.\n.\n.\n.\nПохороны',
    7: 'Урок математики. \nУчительница: \n-Дети, решаем задачи. Петя, встань. \nПетя встал. \n-Петя, у тебя было пять карандашей, у твоего друга было шесть карандашей. Ты поделился с другом тремя карандашами, а он потом дал тебе четыре. Сколько у вас у всех карандашей? \n-У друга пять, у меня шесть. \n-Правильно, Петя, садись, пятёрка тебе. Лизочка, встань, будь добра. \nЛиза встала. \n-Лиза, у тебя было три карандаша, у твоего друга было семь. Ты ему дала два карандаша, а потом он тебе тоже два. Сколько у вас у всех карандашей? -У друга семь, у меня три. \n-Правильно, Лиза, садись, пятёрка тебе. Вовочка, встань, пожалуйста.\n-Сама встань!\nВовочке дали Героя социалистического труда.',
    8: 'Как называется драка между школьниками из параллелей?\n.\n.\n.\n.\n.\n.\nКлассовая борьба',
    9: 'Пять англичан в Ауди Quattro приехали на пост ирландской границы. Таможенник останавливает их и говорит:\n— Впятером в Quattro ездить нельзя.\n— Почему нельзя?!\n— Quattro значит четыре.\n— Quattro просто название автомобиля, — пытается возразить англичанин, не веря своим ушам. — Посмотрите в документы, эта машина рассчитана на пятерых.\n— Не надо мне рассказывать, — говорит таможенник. — Quattro значит четыре. У вас в машине 5 человек, значит вы нарушаете закон.\n— Идиот!!! Позовите начальника, я поговорю с кем-нибудь кто поумнее на этой таможне!\n— Извините, начальник занят. Он выясняет какого чёрта в УАЗ Патриот залез либерал.',
    10: 'Внучок начинает лезть на дерево и дед его спрашивает:\n- Нафига ты на дерево лезешь?\n- Яблоки кушать\n- Так это берёза, идиот\n- А они у меня с собой',
    11: 'На море тонет корабль, пассажиры садятся на шлюпки, их не хватает. Тут, всех расталкивая, проходит Сталин и садится в шлюпку. Ему все кричат: "Как вы так можете, на корабле еще остались дети!"\nОн в ответ им говорит:\n–Спасибо, товарищи, я не голоден',
    12: 'Идут два немых и один другому говорит: \n- Слушай, а ты чего молчишь?\n- Так я ж немой',
    13: 'Пять англичан в Ауди Quattro приехали на пост ирландской границы. Таможенник останавливает их и говорит:\n— Впятером в Quattro ездить нельзя.\n— Почему нельзя?!\n— Quattro значит четыре.\n— Quattro просто название автомобиля, — пытается возразить англичанин, не веря своим ушам. — Посмотрите в документы, эта машина рассчитана на пятерых.\n— Не надо мне рассказывать, — говорит таможенник. — Quattro значит четыре. У вас в машине 5 человек, значит вы нарушаете закон.\n— Идиот!!! Позовите начальника, я поговорю с кем-нибудь кто поумнее на этой таможне!\n— Извините, начальник занят. Он выясняет какого чёрта в Линкольне оказался Кеннеди',
    14: 'Как называется мистическое существо, поселившееся в кальянной?\n.\n.\n.\n.\n.\n.\nДымовой',
    15: 'Внимание, добрый анекдот:\n\n– Помнишь ты год назад котенка потерял? Есть две новости: хорошая и плохая\n— Давай плохую\n— Нет у тебя больше котёнка\n— А хорошая?\n— У тебя есть кот!\n\nИ даёт ему выросшего кота, и всё у них хорошо, и слава тебе, Господи.',
    16: 'Идёт сотрудник военкомата, на встречу ему Дима.\n-Ты кто? - Я Дима. -Записываю: Дима. Придёшь ко мне завтра утром, я тебя мобилизирую.\nДима заплакал. Идёт сотрудник дальше, навстречу Саша.\n- Ты кто? - Я Саша.\n- Записываю: Саша. Придёшь ко мне сегодня днём, я тебя мобилизирую.Саша заплакал. Идёт лев дальше, навстречу ему Петька.- Ты кто? - Я Петька.\n- Записываю: Петька. Придёшь ко мне завтра вечером, я тебя мобилизирую!- А можно не приходить?\n- Можно. Вычёркиваю...\nНа следующее утро у Петьки обнаружили 10 кг кокаина.',
    17: '— Наум Аронович, и почему вы такой грустный?\n— Сын женится.\n— Зачем грустить, у других тоже сыновья женятся. И какое имя невесты?\n— Степан.\n— Да, действительно не еврейское имя.',
    18: 'Первый человек, гуляя по райскому саду, обратился к Богу:\n— Боже, а дашь мне имя?\n— А дам.',
    19: '— Тетя Соня! Зачем ваш Яша ходит в музыкальную школу?! У него же нет никакого слуху!\n— Дуpак! Яша ходит туда не слухать! Яша ходит туда игpать!',
    20: 'Поспорили как то американец и русский, чья комната страха страшнее. Зашел, значит, русский в их комнату: скелеты всякие, привидения – в общем, ничего интересного.\nЗаходит теперь американец к нам, видит: длиннющий темный коридор, а в самом конце грузин на корточках сидит, в руке держит горящую свечку.\nГрузин:\n- Попа мыл?\n- Нет\nГрузин молча достаёт тазик с водой..',
    21: 'Если вы вечером стоите за спиной человека, который получает деньги из банкомата, и не хотите, чтобы он вас боялся, легонько поцелуйте его в шею.',
    22: 'В кафе заходит человек с собакой и заключает с посетителями пари, что его пёс сейчас будет разговаривать. Но собака молчит. Человек оплачивает пари и уходит под общий хохот.\n— Из-за тебя я проиграл уйму денег! — говорит хозяин псу, — Почему ты не заговорил?\n— А о чем с этими обрыганами разговаривать?\n— И то верно',
    23: 'Сидит мужик на базаре, продаёт порошок от мышей, народ собрался, покупают, под конец почти ничего не осталось, подходит парень и спрашивает:\n- А как им пользоваться?\n- Ловишь мышь, бросаешь ей горсть порошка в глаза, вскоре мышь умирает.',
    24: '— Это служба поддержки?\n— Да\n— Я хочу пива\n— Поддерживаю',
    25: 'Когда подорожал бензин, я молчал - я не был водителем\nКогда подорожала домашняя техника, я молчал - меня и своя устраивала\nКогда подорожала медицина, я молчал - я был здоров\nКогда подорожали Вафельные Трубочки Яшкино 190гр Ореховые, вступиться за меня было уже некому',
    26: 'Сидят два 70 летних грузина, один другому говорит:\n— Гиви, я такой-же сильный как и 40 лет назад\nГиви:\n— С чего ты взял?\n— Видишь вон тот камень? Я тогда его поднять не мог... И сейчас не могу',
    27: '- Не приняли меня в университет, Василий Иваныч, на истории срезался. Спросили меня, кто такой Цезарь, а я возьми и ляпни, что это жеребец пятого эскадрона. \n- Моя вина, Петька. Когда тебя не было, я его в седьмой перевел.',
    28: 'Заикающийся ведущий новостей уже несколько часов интригует всю страну',
    29: '-Изя, сколько будет семь на восемь? \n-А мы продаем или покупаем?',
    30: 'Урок биологии.\n- Петров, назови двух хищников.\n- Тигр и... не знаю...\n- Двойка. Иванов, назови трёх хищников.\n\n- Садись, двойка. Рабинович! Пять хищников.\n- Два тигра и три льва!',
}

url_error: dict[int: str] = {
    1: 'Неправильный URL',
    2: "Извините, но что-то пошло не так.\nПопробуйте отправить ссылку на другое видео",
    3: "Нельзя отправлять стрим",

}
