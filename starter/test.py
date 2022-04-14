# Import time library
import time as t


## Countdown function starts here
def stopwatch(sec):
    while sec:
        minn, secc = divmod(sec, 60)
        timeformat = '{:02d}:{:02d}'.format(minn, secc)
        print(timeformat, end='\r')
        t.sleep(1)
        sec -= 1


print('Goodbye!\n')
## calling stopwatch function
stopwatch(15)
