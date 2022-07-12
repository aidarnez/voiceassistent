import speech_recognition
import os
import sys
import webbrowser
import pyautogui
import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5
with speech_recognition.Microphone() as mic:
    sr.adjust_for_ambient_noise(source=mic, duration=0.1)
    audio = sr.listen(source=mic)
    query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
    print(query)


def pos(word, morth=pymorphy2.MorphAnalyzer()):
    return morth.parse(word)[0].tag.POS


words = [morph.parse(word)[0].normal_form for word in query.split()]
for word in words:
    if morph.parse(word)[0].tag.POS in ['INTJ', 'PRCL', 'CONJ', 'PREP']:
        words.remove(word)
s = ''
for i in words:
    s += ' ' + i
words = s.replace(' ', '', 1)


def execute_cmd(cmd, request=''):
    if cmd == 'taskmgr':
        os.system('taskmgr.exe')
    if cmd == 'stop':
        sys.exit('Программа завершена')
    if cmd == 'control':
        os.system('start control')
    if cmd == 'search':
        request = request.split()
        search = 'https://yandex.ru/search/?text='
        for word in request:
            search += '+' + word
        webbrowser.open_new(search)
    if cmd == 'homepath':
        os.system('explorer /n, "%Userprofile%')
    if cmd == 'mute':
        pyautogui.press('volumemute')
    if cmd == 'sum':
        request = request.replace(',', '.')
        result = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", request)
        for j in range(len(result)):
            result[j] = float(result[j])
        print(sum(result))


taskmgr = 'диспетчер задача'
control = 'панель управление'
homepath = 'папка пользователь'
cmds = {
    "search": ('поиск интернет', 'найти интернет',),
    "taskmgr": ('открыть ' + taskmgr, 'запустить ' + taskmgr, 'запуск ' + taskmgr, 'начало ' + taskmgr,
                'активация ' + taskmgr, 'открытие ' + taskmgr, 'активировать ' + taskmgr, 'начать ' + taskmgr,
                'включить ' + taskmgr, 'включение ' + taskmgr, 'зайти ' + taskmgr),
    "stop": ('стоп', 'остановить', 'деактивация', 'закрыть', 'остнановка', 'закрытие', 'stop'),
    "control": ('открыть ' + control, 'запустить ' + control, 'запуск ' + control, 'начало ' + control,
                'активация ' + control, 'открытие ' + control, 'активировать ' + control, 'начать ' + control,
                'включить ' + control, 'включение ' + control, 'зайти ' + control, 'перейти ' + control,
                'переход ' + control),
    "homepath": ('открыть ' + homepath, 'запустить ' + homepath, 'запуск ' + homepath, 'начало ' + homepath,
                 'активация ' + homepath, 'открытие ' + homepath, 'активировать ' + homepath, 'начать ' + homepath,
                 'включить ' + homepath, 'включение ' + homepath, 'зайти ' + homepath, 'перейти ' + homepath,
                 'переход ' + homepath),
    "sum": ('+', 'сумма', 'сложить', 'сложение', 'сложение', 'плюс'),
    "mute": ('выключить звук', 'выключение звук', 'отключи звук', 'включить звук', 'включение звук')
}
if any(word in words for word in cmds["search"]):
    query = query.replace('поиск в интернете', '')
    query = query.replace('найти в интернете', '')
    execute_cmd('search', query)
elif any(word in words for word in cmds["taskmgr"]):
    execute_cmd('taskmgr')
elif any(word in words for word in cmds["stop"]):
    execute_cmd('stop')
elif any(word in words for word in cmds["control"]):
    execute_cmd('control')
elif any(word in words for word in cmds["homepath"]):
    execute_cmd('homepath')
elif any(word in words for word in cmds["mute"]):
    execute_cmd('mute')
elif any(word in words for word in cmds["sum"]):
    execute_cmd('sum', query)
else:
    print('Простите, я не знаю такую команду')
