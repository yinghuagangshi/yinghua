import win32api
import win32process

win32process.SetProcessAffinityMask(win32api.GetCurrentProcess(),1)