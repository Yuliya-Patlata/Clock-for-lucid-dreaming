'''
Программа-будильник для осознанных снов
Время окончательного подъема wake_up  громким звуком  мелодиии
Tool_Lateralus задается
пользователем например 8:30:00 (для  тестирования указвать wake_up
на 4-7 минут больше текущего).
Программа должна запрашивать у  пользователя  кол-во
часов lucid_duration планируемых для практики осознанных  снов
перед временем
окончательного пробуждения wake_up (для  тестирования указывать
lucid_duration 2-5 минут)
float, и начиная с вычисленного  времени тихого будильника
first_ring в форммате "% H:% M : %S ',
например с 4:30:00, периодически подбуживать спящего слегка
слышимой сквозь сон
вибацией звука варгана vargan_low, с заданным интервалом
lucid_interval ( например 40 минут
(для  тестирования указывать lucid_interval 40 - 170 секунд,
поскольку длительность  мелодии варгана 28 сек   )) .
'''

# https://realpython.com/playing-and-recording-sound-python/
# from os import system  # работает под виндой
from pydub import AudioSegment  # под линукс работает, а под виндой не знаю
from pydub.playback import play  # под линукс работает,  а под виндой не знаю
from datetime import datetime, timedelta


def convert_ring(ring_hms_str):

    #Узнаем текущую дату,которую нужно прибавить к часам и минутам будильника
    str_now_dmy = datetime.now().strftime("%d.%m.%Y")
    print('str_now_dmy = ', str_now_dmy, type(str_now_dmy))

    # Формируем полную  строку времени будильника
    ring_str_full = str_now_dmy + ' ' + ring_hms_str
    print('ring_str_full : ', ring_str_full)

    # Конвертируем полную  строку времени будильника в datetimeobject
    ring = datetime.strptime(ring_str_full, "%d.%m.%Y %H:%M:%S")
    print('ring', ring)
    time_of_setting = datetime.now()

    if ring >= time_of_setting:
        print('Ring will be  today')
        return ring
    else:
        ring = ring + timedelta(hours=24)
        print('Ring will be  tomorrow', ring)
        return ring


def roundSeconds(dateTimeObject):
    newDateTime = dateTimeObject
    #print('newDateTime.second : ', newDateTime.second)

    if newDateTime.second >= 0.5:
        newDateTime = newDateTime + timedelta(seconds=1)
    return newDateTime.replace(microsecond=0)


class FirstRingError(Exception):
    def __init__(self):
        Exception.__init__(self)


class LucidIntervalError(Exception):
    def __init__(self):
        Exception.__init__(self)


class LucidDurationError(Exception):
    def __init__(self):
        Exception.__init__(self)


def main():
    try:
        wake_up_str = input('Input wake up time in format "00:00:00", для \
        тестирования указвать wake_up \n на 4-7 минут больше \
        текущего \n wake_up_str => ')
        wake_up = convert_ring(wake_up_str)
        print(type(wake_up), wake_up)

        lucid_duration = float(input('Input total approximate planned duration \
        of \n lucid_dreaming in hours ( для  тестирования указывать \
        lucid_duration 2-5.1 минут): lucid_duration => '))

        #для теста в строке ниже указаны минуты, а вообще будут часы hours lucid_duration
        first_ring = wake_up - timedelta(minutes=lucid_duration)
        print('The time of first quiet ring will be :', first_ring)

        lucid_interval = int(input('Input interval of quiet rings in \
        \n minutes, which will ring throught planned \n duration of \
        lucid_dreaming lucid_interval \n ( для  тестирования указывать\
        lucid_interval 150 - 170 секунд)  =>'))

        print("For EOFError you may press ctrl-d")
        print("For EOFError you may press ctrl-F2")

        cur_time = roundSeconds(datetime.now())

        if first_ring >= wake_up or first_ring <= cur_time:
            print('\n Error description :')

            if first_ring <= datetime.now():
                print('The 1-st_ring must be bigger than now, input shorter lucid_duration')
            elif first_ring >= wake_up:
                print('The 1-st_ring must be less than wake_up')

            raise FirstRingError()

        if first_ring + timedelta(seconds=lucid_interval) >= wake_up:
            print('\n Error description :')
            print('Input shorter lucid_interval, otherwise quite ring will never sound')
            raise LucidIntervalError()

        if wake_up - timedelta(minutes=lucid_duration) <= datetime.now():
            print('\n Error description :')
            print('Input shorter lucid_duration, quite ring must not be before now')
            raise LucidDurationError()

    except EOFError:
        print('Ну зачем вы сделали мне EOF?')
    except KeyboardInterrupt:
        print('Вы отменили операцию.')
    else:
        next_ring = first_ring
        print('cur_time =', cur_time)
        print('next_ring = ', next_ring)
        print('wake_up = ', wake_up)
        print('cur_time <= wake_up ? =>', cur_time <= wake_up)
        quiet_sound_duration = 102  # seconds

        while cur_time <= wake_up:

            if next_ring + timedelta(seconds=quiet_sound_duration) < wake_up:

                if cur_time == next_ring:
                    print('NOW I am in lucid dream, cur_time', cur_time)
                    print('QUIET SOUND', datetime.now())
                    # для тестирования в строке ниже сек,а вообще будут мин
                    next_ring = next_ring + timedelta(seconds=lucid_interval)
                    print('next_quiet_ring will be :', next_ring)
                    # system('vargan_low.mp3') # for windows бесконечном цикле
                    sound = AudioSegment.from_mp3('vargan_low.mp3')
                    play(sound)

            else:

                if roundSeconds(datetime.now()) == wake_up:
                    print('NOW I am in WAKE UP cur_time', cur_time)
                    print('LOUD SOUND', datetime.now())
                    # system('Tool_Lateralus.mp3') # for windows
                    sound = AudioSegment.from_mp3('Tool_Lateralus.mp3')
                    play(sound)

            cur_time = roundSeconds(datetime.now())


if __name__ == "__main__":
    main()