#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from glob import glob
import os, sys
from os.path import expanduser
import curses
import subprocess as sp
from pathlib import Path
import re
from subprocess import Popen, PIPE, STDOUT
import shlex
import shutil


def check_fname(fname):
    name = fname.split('.')[0]
    if re.fullmatch(r'.*_\d{6}[a-z]?$', name) == None:
        return False
    else:
        return True

def rename(fpath):

    date_pattern = '_' + datetime.date.today().strftime('%y%m%d')
    fname = fpath.split('/')[-1]
    if date_pattern in fname:
        if re.fullmatch(r'.*_\d{6}$', fname.split('.')[0]) == None:
         
            pass
        else:
            # 末尾がYYMMDDで同日　："_YYMMDDa"に変更
            return fname.split('.')[0] + 'a.' + fname.split('.')[1]
    # 同日以外　fnameに"_YYMMDD"が既に含まれているかチェック
    elif (check_fname(fname) == True):
        fname = '_'.join(fname.split('.')[0].split('_')[:-1]) + '.' + fname.split('.')[1]
    fname_wdate = fname.split('.')[0] + date_pattern + '.' + fname.split('.')[1]
    return fname_wdate
    #elif len(glob.glob('test.txt')) == 0: # + fname.split('.')[0] + '_*.' + fname.split('.')[1]):
    #    return fname_wdate+"eee"
    #if os.path.exists("./" + fname):
    #    return fname_wdate
        
class exls:
    def __init__(self, stdscr):
        # ==================
        # Check OS
        # ==================
        if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
            self.crr_os = "win"
        elif sys.platform.startswith('darwin'):
            self.crr_os = "mac"

        # Initialize variables
        self.find_status = False
        self.find_cmd = ""
        self.df_cmd = "df -h"
        self.external_flag = False
        self.send_cmd = True
        self.cur_path = ""
        self.cur = 1
        self.offset = 0
        self.p_path = "."
        self.cut_fpath = "" 
        self.copy_fpath = ""
        self.ls_cmd = "ls -Ghpt"
        self.list = []
        self.all_list = []
        self.max_disp = stdscr.getmaxyx()[0]


    def init(self, stdscr, cur, offset, max_disp):
        cur = 1
        offset = 0
        max_disp = stdscr.getmaxyx()[0]
        return cur, offset, max_disp

    def get_filename(self, line, ls_cmd, external_flag):
        if "-l" in ls_cmd:
            return " ".join(line.split()[7:])
        elif external_flag:
            return " ".join(line.split()[5:])
        else:
            return line

    def key_input(self, stdscr, key):
        self.send_cmd = False
        # ==================
        # Quit
        # ==================
        if key == ord('q'):
            if self.crr_os == "mac":
                Path(str(os.path.dirname(__file__))+"/." + self.cur_path.replace("/", "^")).touch()
            elif self.crr_os == "win":
                Path(str(os.path.dirname(__file__))+"\\.^" + self.cur_path.replace('\\', "^").replace(':', "")).touch()
            return False  # Exit the while()

        # ==================
        # Up/Down cursor 
        # ==================
        elif key == ord('k'): #UP:
            if self.cur > 1: self.cur = self.cur - 1
            elif (self.cur == 1)&(self.offset > 0):
                self.offset = self.offset - 1
            return True
        elif key == ord('j'): #DOWN:
            if self.cur < len(self.list)-1: self.cur = self.cur + 1
            elif (self.cur >= len(self.list) - 1)&(self.cur + self.offset != len(self.all_list) - 1):
                self.offset = self.offset +1
            return True

        # ==================
        # Open explorer    
        # ==================
        elif key == ord('o'):
            if self.crr_os == "mac":
                sp.call(["open", "."])
            elif self.crr_os == "win":
                sp.call(["explorer", "."])
            return True
        # ==================
        # Cut/Copy
        # ==================
        elif key == ord('x'): # Cut
            self.copy_fpath = ""
            self.cut_fpath = self.cur_path + "/" + self.get_filename(self.list[self.cur], self.ls_cmd, self.external_flag)
            return True
        elif key == ord('c'): # Copy
            self.cut_fpath = ""
            self.copy_fpath = self.cur_path + "/" + self.get_filename(self.list[self.cur], self.ls_cmd, self.external_flag)
            return True

        # from here, it needs refresh
        self.send_cmd = True
        self.find_status = False
        # ==================
        # Enter/Execute
        # ==================
        if key == ord('n'):
            name = self.get_filename(self.list[self.cur], self.ls_cmd, self.external_flag)
            if self.external_flag: 
                self.external_flag = False
                if name.endswith("/"):
                    # C drive always endswith "/"
                    drive_name = "c:"
                else:
                    # ex. "/d" to "d:" for D drive
                    drive_name = name[1] + ":"
                os.chdir(drive_name)

            elif (name.endswith("@")) or (os.path.isdir(name)):
                os.chdir(name)
            else:
                if self.crr_os == "mac":
                    sp.call(["open", name])
                elif self.crr_os == "win":
                    self.fpath = self.cur_path + "\\" + '"' + name + '"'
                    sp.run(["start", self.fpath], shell=True)
        # ==================
        # Add/Remove option of "ls"
        # ==================
        elif key == ord('.'): # "-A" option
            if "A" in self.ls_cmd:
                self.ls_cmd = re.sub("A","", self.ls_cmd)
            else:
                self.ls_cmd = self.ls_cmd + "A"
        elif key == ord('l'): # "-l" option
            if "-l" in self.ls_cmd:
                self.ls_cmd = re.sub("-l","-", self.ls_cmd)
            else:
                self.ls_cmd = re.sub("-","-l", self.ls_cmd)
        elif key == ord('t'): # "-t" option
            if "t" in self.ls_cmd:
                self.ls_cmd = re.sub("t","", self.ls_cmd)
            else:
                self.ls_cmd = self.ls_cmd + "t"
        elif key == ord('s'): # "-S" option
            if "S" in self.ls_cmd:
                self.ls_cmd = re.sub("S","", self.ls_cmd)
            else:
                self.ls_cmd = self.ls_cmd + "S"
        # ==================
        # Paste
        # ==================
        elif key == ord('v'): # Paste
            if self.cut_fpath != "":
                # cut command
                if not os.path.exists("./" + self.cut_fpath.split("/")[1]):
                    shutil.move(self.cut_fpath, ".")            
            elif self.copy_fpath != "":
                # copy command
                # file not exist
                if not os.path.exists("./" + self.copy_fpath.split("/")[1]):
                    shutil.copy2(self.copy_fpath, ".")            
                # file exist
                else:
                    copy_fname = rename(self.copy_fpath)
                    shutil.copy2(self.copy_fpath, "./" + copy_fname)            
        
            # clear file path
            self.cut_fpath = ""
            self.copy_fpath = ""

        # ==================
        # Change Directory
        # ==================

        # Up to parent directory
        if key == ord('u'):
            os.chdir("..")
        # list External device
        elif key == ord('e'):
            if self.crr_os == "mac":
                os.chdir("/Volumes/")
            elif self.crr_os == "win":
                self.external_flag = True
        # Back to previoius path
        elif key == ord('b'):
            os.chdir(self.p_path)
        # move to Home
        elif key == ord('h'):
            os.chdir(os.path.dirname(expanduser("~/")))
        # move to Project
        elif key == ord('p'):
            os.chdir(os.path.dirname(expanduser("~") + "/data/"))
        # move to Favorite
        elif key == ord('f'):
            os.chdir(os.path.dirname(os.path.abspath(__file__))+"/fav")
        # move to Web
        elif key == ord('w'):
            os.chdir(os.path.dirname(os.path.abspath(__file__))+"/web")
        # move to Desktop
        elif key == ord('d'):
            os.chdir(os.path.dirname(expanduser("~") + "/Desktop/"))
        # find files/directory
        elif (key >= ord('A'))&(key<= ord('Z')):
            self.find_status = True
            self.find_cmd = 'find . -iname "' + chr(key) + '*" -depth 1 | xargs ls -Al -depth'
        self.cur, self.offset, self.max_disp = self.init(stdscr, self.cur, self.offset, self.max_disp)
        self.p_path = self.cur_path
        return True

    def draw(self, stdscr):

        # loop until enter 'q' key
        while 1:
            # Check command and get list
            if self.send_cmd:            
                if self.find_status:
                    self.all_list = sp.check_output(self.find_cmd, stderr=sp.STDOUT, shell=True).decode('utf-8').split('\n')
                    self.all_list = [s for s in self.all_list if ": " not in s]
                    self.all_list.insert(0,"")
                    self.list = self.all_list[self.offset:self.offset + self.max_disp -1]
                elif self.external_flag:
                    self.all_list = sp.check_output(self.df_cmd, shell=True).decode('utf-8').strip().split('\n')
                    self.list = self.all_list[self.offset:self.offset + self.max_disp -1]
                else:
                    self.all_list = sp.check_output(self.ls_cmd, shell=True).decode('utf-8').strip().split('\n')
                    if ("-l" not in self.ls_cmd):
                        if (self.all_list[0] == ""):
                            self.list = [""," "]
                        else:
                            self.all_list.insert(0, "") # add self.offset to adjust display
                            self.list = self.all_list[self.offset:self.offset + self.max_disp -1]
                    else:
                        self.list = self.all_list[self.offset:self.offset + self.max_disp -1]
            else:
                self.list = self.all_list[self.offset:self.offset + self.max_disp -1]
            self.cur_path = os.getcwd()
            stdscr.clear()
            # ==================
            # Drawing
            # ==================
            for i, file in enumerate(self.list):
                if ((i == 0) & (not self.external_flag)):
                    stdscr.addstr(i, 0, self.cur_path)
                    stdscr.addstr(i, 40, str(self.cut_fpath))
                else:
                    if i == self.cur:
                        if file.endswith("/"): 
                            stdscr.addstr(i, 0, file[:-1], curses.color_pair(4))
                        elif file.endswith("xls") | file.endswith("xlsx"):
                            stdscr.addstr(i, 0, file, curses.color_pair(5))
                        elif file.endswith("pdf"):
                            stdscr.addstr(i, 0, file, curses.color_pair(6))
                        else:
                            stdscr.addstr(i, 0, file, curses.A_STANDOUT)
                    else:
                        if file.endswith("/"):                    
                            stdscr.addstr(i, 0, file[:-1], curses.color_pair(1))
                        elif file.endswith("xls") | file.endswith("xlsx"):
                            stdscr.addstr(i, 0, file, curses.color_pair(2))
                        elif file.endswith("pdf"):
                            stdscr.addstr(i, 0, file, curses.color_pair(3))
                        else:
                            stdscr.addstr(i, 0, file)
            stdscr.refresh()
            if self.key_input(stdscr, stdscr.getch()) == False:
                break

def main(stdscr):
    # ==================
    # Initialize curses
    # ==================
    #curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_RED)

    exls(stdscr).draw(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)