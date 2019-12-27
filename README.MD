
# esp-setup

simplified setup up for esp8266 / esp32 device 

# how it works

the tool discovers first the connected device type with `esptool.py` and
searches then the available firmware `bin` files in your download folder.
the search follows the naming convention of the micropython release (alphabetical sort).

after that it ask which to install.

optional you can erase flash before installing


## cmd line

display all available cmd line options with


    python3 -m espsetup -h

    usage: espsetup [options]

    setup an esp32/esp8266 device

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show version info and exit
      -s, --dry             simulate /dry run, only show cmd information
      -port PORT, -p PORT   port/device to use (default: /dev/ttyUSB0)
      -baud BAUD, -b BAUD   baud rate to use (default: 115200)
      -c {ask,y,yes,n,no}, -erase_flash {ask,y,yes,n,no}
                            erase_flash before installing (default: ['ask'])
      -image IMAGE, -i IMAGE
                            image to install, use 'latest' to install the last
                            version available in your folder(default: show list of
                            available images '*.bin')
      -dir IMAGE_DIR, -d IMAGE_DIR
                            image search directory (default: ~/Downloads)

