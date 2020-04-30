#!/usr/bin/env python3

import os
import sys

import glob
import argparse

VERSION="v0.0.4"


def espsetup():
    
    port = '/dev/ttyUSB0'
    baud = 115200

    parser = argparse.ArgumentParser(prog='espsetup', usage='%(prog)s [options]',
                                     description='setup an esp32/esp8266 device')
    parser.add_argument("-v", "--version", dest='show_version', action="store_true",
                        help="show version info and exit", default=False )
    parser.add_argument("-s", "--dry", dest='dry_run', action="store_true",
                        help="simulate /dry run, only show cmd information", default=False )

    parser.add_argument("-port", "-p", type=str, dest='port', action="store",
                        help="port/device to use (default: %(default)s)", default=port )
    parser.add_argument("-baud", "-b", type=int, dest='baud', action="store",
                        help="baud rate to use (default: %(default)s)", default=baud )

    parser.add_argument("-c", "-erase_flash", dest='erase_flash', action="store", 
                        choices=["ask", "y", "yes","n", "no"], nargs=1,
                        help="erase_flash before installing (default: %(default)s)", default=['ask'] )
    
    parser.add_argument("-image", "-i", dest='image', action="store",
                        help="image to install, use 'latest' to install the last version"
                        + " available in your folder"
                        + "(default: show list of available images '*.bin')"
                        , default=None )
    parser.add_argument("-dir", "-d", dest='image_dir', action="store",
                        help="image search directory (default: %(default)s)", default="~/Downloads" )

    args = parser.parse_args()

    if args.show_version:
        print( "Version:", VERSION )
        return
        
    PORT = args.port
    BAUD = args.baud
    IMAGEDIR = args.image_dir
    IMAGE = args.image
    erase_flash = args.erase_flash[0]
    simulate = args.dry_run

    is_esp = False
    is_8266 = False
    is_32 = False

    print( f"getting micropython system information port:{PORT}" )

    with os.popen( f"esptool.py --port {PORT} chip_id" ) as p:
        resp = p.read()
        print(resp)
        r = resp.lower()
        is_esp = r.find("esp") >= 0        
        is_8266 = r.find("esp8266") >= 0  
        is_32 = r.find("esp32") >= 0  

    if not( is_8266 ^ is_32 ):
        print("exit")
        sys.exit(1)

    allimages = glob.glob( os.path.expanduser(f"{IMAGEDIR}/esp[32|8266]*.bin") )
    flt = "esp32" if is_32 else "esp8266"

    allimages = list(filter( lambda x : x.find(flt)>=0, allimages ))

    if len(allimages)==0:
        print( f"no images found in {IMAGEDIR}" )
        sys.exit(1)

    allimages.sort()
    allimages.reverse()

    def printselection():
        print( "choose an image" )
        hl = ">"
        for i,img in enumerate(allimages):
            print( hl, i, img )
            hl = " "

    if IMAGE=='latest':
        IMAGE = allimages[0]        
        
    if IMAGE is None:
        while True:
            imgno = 0
            while True:
                printselection()
                try:        
                    imgno = input( "enter no to install [0]? " ).strip()
                    if len(imgno)==0:
                        imgno = "0"                        
                    imgno = int(imgno)
                    break
                except KeyboardInterrupt as ex:
                    raise ex
                except:
                    pass
    
            try:
                IMAGE = allimages[imgno]
            except:
                continue
            r=input( f"do you want to install {IMAGE} y/[n]? " ).strip()
            if len(r)==0:
                r = "n"
            if r=="y":
                break

    print(f"install {IMAGE}")
        
    image_ok = False

    cust = ""

    if is_32:
        cust = "-z 0x1000"
        image_ok = IMAGE.find("esp32") >= 0 

    if is_8266:
        cust = "--flash_size=detect 0"
        image_ok = IMAGE.find("esp8266") >= 0 

    if not image_ok:
        print( "wrong image" )
        sys.exit(0)
     
    def runcmd(cmd):
        print( "excute:", cmd )
        if simulate:
            return
        p = os.popen( cmd ) 
        while True:
            resp = p.readline()
            if len(resp)==0:
                break
            print(resp, end = '')
        r = p.close()
        if r != None:
            print( "failed, error code", r )
            sys.exit(r)

    if erase_flash == "ask":
        erase_flash = input("erase_flash now [y]/n? ").strip()
        
    if len(erase_flash)==0 or erase_flash in ['y', 'yes']:        
        cmd = f"esptool.py --port {PORT} erase_flash"
        runcmd(cmd)

    cmd = f"esptool.py --port {PORT} --baud {BAUD} write_flash {cust} {IMAGE}"
    runcmd(cmd)

    return args


if __name__=='__main__':
    
##    sys.argv = "espsetup.py -c ask -i latest ".split()
    
    args = espsetup()
    
    