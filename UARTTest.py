import HeadlessClasses
import time

UART_MONITOR_ID = 0x01
UART_MONITOR_NAME = "Test incubator"

counter=1

while True:
    uart = HeadlessClasses.MyUART(1)
    while True:
        s = "Counter: %d" % (counter)
        counter=counter+1
        uart.Write(s)
        print(s)
        time.sleep(2)

