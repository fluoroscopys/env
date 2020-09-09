import sys
import os
import datetime
import time
import json
from keyhac import *

def os_check():    
    if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
        import pyauto
        return "win"
    elif sys.platform.startswith('darwin'):
        return "mac"
    return ""

def configure(keymap):
    start = time.time()
    # Theme
    keymap.setTheme("black")
    # Defining virtual keycode 255 as User-modifier-0
    keymap.defineModifier( 255, "User0" )

    # Global keymap which affects any windows
    keymap_global = keymap.defineWindowKeymap()
    crr_os = os_check()

    #########################################
    #
    # OS : Windows
    #
    #########################################
    if crr_os == "win":
        # --------------------------------------------------------------------
        # Text editer setting for editting config.py file

        # Setting with program file path (Simple usage)
        keymap.editor = os.path.join(ckit.ckit_misc.getAppDataPath(), r"..\Local\Programs\Microsoft VS Code\Code.exe")
        # --------------------------------------------------------------------
        # Customizing the display
        # Font
        keymap.setFont( "Meiryo", 11 )
        # Simple key replacement
        keymap.replaceKey( "RAlt", 235 )
        keymap.replaceKey( "29", 236 ) # 無変換キーに仮想コード236を割り当て
        # User modifier key definition
        keymap.defineModifier( 235, "U0" )
        keymap.defineModifier( 236, "U1" )
        # ----------------------------------------
        #  Launchers
        # ----------------------------------------
        def disp_chrome():
            active_window = keymap.ActivateWindowCommand( "chrome.exe" )
            if active_window() == None:
                executeFunc = keymap.ShellExecuteCommand(None, r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "--start-fullscreen", "" )
                executeFunc()
        keymap_global[ "User0-B" ] = disp_chrome
        def disp_vscode():
            active_window = keymap.ActivateWindowCommand( "code.exe" )
            if active_window() == None:
                executeFunc = keymap.ShellExecuteCommand(None, os.path.join(ckit.ckit_misc.getAppDataPath(), "..\Local\Programs\Microsoft VS Code\Code.exe"), "", "" )
                executeFunc()
        keymap_global[ "User0-V" ] = disp_vscode
        
        home_dir = getProfilePath()
        keymap_global[ "LWin-E" ] = keymap.ShellExecuteCommand(None, r"explorer", home_dir, "" )
        if 0:
            def disp_date():
                keymap.setFont( "Meiryo", 14 )
                keymap.popBalloon("ime_status", datetime.datetime.today().strftime("%m/%d %H:%M"), 5000)
            keymap_global[ "User0-Space" ] = disp_date
        # ----------------------------------------
        #  Mouse
        # ----------------------------------------
        # USER0-Alt-Up/Down/Left/Right/Space/PageUp/PageDown : Virtul mouse operation by keyboard
        keymap_global[ "User0-LWin-J"  ] = keymap.MouseMoveCommand(-10,0)
        keymap_global[ "User0-LWin-L" ] = keymap.MouseMoveCommand(10,0)
        keymap_global[ "User0-LWin-I"    ] = keymap.MouseMoveCommand(0,-10)
        keymap_global[ "User0-LWin-K"  ] = keymap.MouseMoveCommand(0,10)
        keymap_global[ "D-User0-LWin-U" ] = keymap.MouseButtonDownCommand('left')
        keymap_global[ "U-User0-LWin-U" ] = keymap.MouseButtonUpCommand('left')
        keymap_global[ "D-User0-LWin-O" ] = keymap.MouseButtonDownCommand('right')
        keymap_global[ "U-User0-LWin-O" ] = keymap.MouseButtonUpCommand('right')
        
        # ----------------------------------------
        #  Browser
        # ----------------------------------------
        # Apply the return
        keymap_browser = keymap.defineWindowKeymap( exe_name="chrome.exe")
        keymap_browser[ "User0-I" ] = "Up"
        keymap_browser[ "User0-K" ] = "Down"
        keymap_browser[ "User0-J" ] = "Alt-Left"
        keymap_browser[ "User0-L" ] = "Alt-Right"

        keymap_global[ "User0-1" ] = "PrintScreen"
        def test():
            enter9 = keymap.InputKeyCommand("W-2")
            enter9() 
            enter9 = keymap.InputKeyCommand("left")
            enter9() 
       
            enter = keymap.InputKeyCommand("PrintScreen")
            enter() 
            enter2 = keymap.InputKeyCommand("W-1")
            enter2() 
            enter3 = keymap.InputKeyCommand("W-1")
            enter3() 
            time.sleep(1)
            enter4 = keymap.InputKeyCommand("C-V")
            enter4()
            enter5 = keymap.InputKeyCommand("C-S")
            enter5()
            time.sleep(2)
            enter6 = keymap.InputKeyCommand("Enter")
            enter6()      
            time.sleep(2)
            enter7 = keymap.InputKeyCommand("left")
            enter7()
            time.sleep(2)
            enter8 = keymap.InputKeyCommand("Enter")
            enter8()      



            
        keymap_global[ "User0-space" ] =test

        # ----------------------------------------
        #  Office
        # ----------------------------------------
        keymap_msg = keymap.defineWindowKeymap( exe_name="outlook.exe" )
        # メッセージ貼り付け時のみ引用を適用(現時点未使用)
        def quoteClipboardTextMsg():
            s = getClipboardText()
            if s != None:
                lines = s.splitlines(True)
                if len(lines) > 1:
                    s = ""
                    for i, line in enumerate(lines):
                        if i == 0:
                            s += "\n"+keymap.quote_mark + line
                        else :
                            s += keymap.quote_mark + line
                output = keymap.InputTextCommand(s)
                output()
        if getClipboardText() != None:
            keymap_msg[ "LCtrl-V" ] = quoteClipboardTextMsg
        # Outlook有効時はCtrl+E→Ctrl+F
        keymap_msg[ "LCtrl-F" ] = "LCtrl-E"

        # フォルダ移動
        keymap_msg[ "User0-F" ] = "Alt-H", "M", "V", "O"
        
        # サイドバー表示/非表示 
        keymap_msg[ "Ctrl-B" ] = "Alt-V", "Y", "2", "F", "N"
        keymap_msg[ "S-Ctrl-B" ] = "Alt-V", "Y", "2", "F", "O"

        if 0:
            # Excel実行時のみ以下を適用
            keymap_excel = keymap.defineWindowKeymap( exe_name="excel.exe" )
            # * F2-> Space(不要かも-> 変換できないため他にアサイン？)
            #keymap_excel[ "RShift" ] = "F2"
            # * Alt+Enter -> Enter
            #IME判定
            #if keymap.getWindow().getImeStatus():
            #    keymap_excel[ "Enter" ] = "Alt-Enter"
            # * シート移動はCtrl(+Shift)+Tab
            keymap_excel[ "LCtrl-Tab" ] = "C-PageDown"
            keymap_excel[ "LCtrl-Shift-Tab" ] = "C-PageUp"
            # * IMEの状態にかかわらず行選択、列選択可能

        # ----------------------------------------
        #  Scheduler (Keyhac supports windows only)
        # ----------------------------------------
            if 0:
                def cronPing(cron_item):
                    # Morning
                    # start : 6:00
                    morning_st = datetime.time(6,14,00)
                    morning_ed = datetime.time(6,15,00)
                    if morning_st <= datetime.datetime.now().time() < morning_ed :
                        if crr_os == "win":       
                            playback = keymap.ShellExecuteCommand(None, r"radiko.bat", "", "" )
                            playback()
                        elif crr_os == "mac":
                            playback = pyauto.ShellExecute(None, r"python3 ~/env/priv/py/alarm/radiko.py", "", "" )
                            playback()
                    # ipocheck
                    ipo_st = datetime.time(12,10,00)
                    ipo_ed = datetime.time(12,11,00)
                    if ipo_st <= datetime.datetime.now().time() < ipo_ed :
                        if crr_os == "win": 
                            exe = keymap.ShellExecuteCommand(None, r"C:\Users\tablet\data\ipo\ipo.bat", "", "" )
                        elif crr_os == "mac":
                            exe = keymap.ShellExecuteCommand(None, r"C:\Users\tablet\data\ipo\ipo.bat", "", "" )
                        exe()
                    # Night
                    # start :21:00
                    night_st = datetime.time(21,30,00)
                    night_ed = datetime.time(21,31,00)
                    if night_st <= datetime.datetime.now().time() < night_ed :
                        playback = keymap.ShellExecuteCommand(None, r"radiko\night.bat", "", "" )
                        playback()
                    #print(datetime.datetime.now().strftime("%H:%M:%S"))

                cron_item = CronItem( cronPing, 60.0 )
                CronTable.defaultCronTable().add(cron_item)

    #########################################
    #
    # OS : Mac
    #
    #########################################

    elif crr_os == "mac":
        # --------------------------------------------------------------------
        # Text editer setting for editting config.py file
        keymap.editor = "Visual Studio Code"
        # --------------------------------------------------------------------
        # Customizing the display
        # Font
        keymap.setFont( "Osaka-Mono", 16 )
        # Simple key replacement
        keymap.replaceKey( "RCtrl", 255 )
        # ----------------------------------------
        #  Launchers: None
        # ----------------------------------------
        
        # ----------------------------------------
        #  Hot Keys for Mac OS
        # ----------------------------------------
        # change hot keys
        keymap_global[ "Cmd-Tab" ] = "Ctrl-Tab"
        keymap_global[ "Cmd-Shift-Tab" ] = "Ctrl-Shift-Tab"
        keymap_global[ "Ctrl-Tab" ] = "Cmd-Fn-F1"
#            keymap_global[ "Ctrl-Shift-Tab" ] = "Cmd-Shift-Tab"

        # Maximize / minimize
        keymap_global[ "LCtrl-Up" ] = "Ctrl-Cmd-F"
        keymap_global[ "LCtrl-Down" ] = "Ctrl-Cmd-F"
        keymap_global[ "LCtrl-D" ] = "Fn-F11"            

        # ----------------------------------------
        #  Browser
        # ----------------------------------------
        # うまくいかない
        keymap_browser = keymap.defineWindowKeymap( app_name="Google Chrome")
        keymap_browser[ "User0-U" ] = "Cmd-OpenBracket"
        keymap_browser[ "User0-O" ] = "Cmd-CloseBracket"

    #########################################
    #
    # OS : Common
    #
    #########################################

    # ----------------------------------------
    #  Hot Keys
    # ----------------------------------------

    # USER0-J/I/K/L : Left/Up/Down/Right
    keymap_global[ "User0-J" ] = "Left"
    keymap_global[ "User0-I" ] = "Up"
    keymap_global[ "User0-K" ] = "Down"
    keymap_global[ "User0-L" ] = "Right"

    keymap_global[ "User0-Shift-J" ] = "Shift-Left"
    keymap_global[ "User0-Shift-I" ] = "Shift-Up"
    keymap_global[ "User0-Shift-K" ] = "Shift-Down"
    keymap_global[ "User0-Shift-L" ] = "Shift-Right"

    keymap_global[ "User0-Alt-J" ] = "A-Left"
    keymap_global[ "User0-Alt-I" ] = "A-Up"
    keymap_global[ "User0-Alt-K" ] = "A-Down"
    keymap_global[ "User0-Alt-L" ] = "A-Right"

    # USER0-U/O/Y/H : PageUp/PageDown/Home/End
    keymap_global[ "User0-U" ] = "PageUp"
    keymap_global[ "User0-O" ] = "PageDown"
    keymap_global[ "User0-Y" ] = "Home"
    keymap_global[ "User0-H" ] = "End"

    keymap_global[ "User0-Shift-Y" ] = "Shift-Home"
    keymap_global[ "User0-Shift-H" ] = "Shift-End"

    keymap_global[ "User0-N" ] = "Enter"
    keymap_global[ "User0-M" ] = "Back"

    # USER0-F1 : Reloading config.
    keymap_global[ "User0-Q" ] = keymap.command_ReloadConfig

    # Clipboard history related
    keymap_global[ "User0-Tab" ] = keymap.command_ClipboardList     # Open the clipboard history list
    keymap.quote_mark = "> "                                      # Mark for quote pasting

    # Reset keyhac
    def reset_keyhac():
        keymap.enableHook(False)
        keymap.enableHook(True)
        print("Reset keyhac")
    keymap_global[ "User0-R" ] = reset_keyhac

    # ----------------------------------------
    #  Hot Strings (JIS keyboard)
    # ----------------------------------------

    # 括弧関連
    def between(str):
        output = keymap.InputTextCommand(str)
        output()
        #if keymap.getWindow().getImeStatus():
        if str == '「」':
            enter = keymap.InputKeyCommand("Enter", "Left")
        else:
            enter = keymap.InputKeyCommand("Left")
        enter() 

    # 「」と[]の処理
    def bracket():
        if keymap.getWindow().getImeStatus():
            return between("「」")
        else :
            return between("[]")
    keymap_global[ "OpenBracket" ] = bracket
    
    # ""処理
    def d_quote():
        return between("\"\"")
    keymap_global[ "Shift-2" ] = d_quote
    
    # ''処理
    def quote():
        return between("\'\'")
    keymap_global[ "Shift-7" ] = quote
    
    # ()処理
    def parenthesis():
        return between("()")
    keymap_global[ "Shift-8" ] = parenthesis

    # , (、)処理
    def comma():
        if (keymap.getWindow().getImeStatus()):
            output = keymap.InputTextCommand("、")
            output()
            enter = keymap.InputKeyCommand("Enter")
            enter()
        else:
            output = keymap.InputTextCommand(", ")               
            output()
        
    keymap_global["Comma"] = comma
    
    # 記号の強制半角
    # '!'    
    def exclam():
        output = keymap.InputTextCommand("!")               
        output()
    keymap_global["S-1"] = exclam

    # '#' 
    def sharp():
        output = keymap.InputTextCommand("#")               
        output()
    keymap_global["S-3"] = sharp
   
    # '$' 
    def dollar():
        output = keymap.InputTextCommand("$")               
        output()
    keymap_global["S-4"] = dollar

    # '%' 
    def parcent():
        output = keymap.InputTextCommand("%")               
        output()
    keymap_global["S-5"] = parcent

    # '&'
    def and_():
        output = keymap.InputTextCommand("&")               
        output()
    keymap_global["S-6"] = and_

    # '='
    def equal_():
        output = keymap.InputTextCommand("=")               
        output()
    keymap_global["S-Minus"] = equal_

    # '+'
    def plus_():
        output = keymap.InputTextCommand("+")               
        output()
    keymap_global["S-Semicolon"] = plus_

    # '*'
    def asta():
        output = keymap.InputTextCommand("*")               
        output()
    keymap_global["S-Colon"] = asta

    # ';'
    def semicolon():
        output = keymap.InputTextCommand(";")               
        output()
    keymap_global["Semicolon"] = semicolon

    # ':'
    def colon():
        output = keymap.InputTextCommand(":")               
        output()
    keymap_global["colon"] = colon

    # '_'
    def Underscore():
        output = keymap.InputTextCommand("_")
        output()
    keymap_global["Underscore"] = Underscore
    keymap_global["S-Underscore"] = Underscore

    # '|'
    def pipeline():
        output = keymap.InputTextCommand("|")
        output()
    keymap_global["S-Yen"] = pipeline
    
    # '<'
    def lessthan():
        output = keymap.InputTextCommand("<")
        output()
    keymap_global["S-Comma"] = lessthan

    # '>'
    def greater_than():
        output = keymap.InputTextCommand(">")
        output()
    keymap_global["S-Period"] = greater_than

    # Spaceは変換時に押すスペースと区別ができれば使用可能
    # WindowsではIMEを右クリック→プロパティ→詳細設定→全般タブにある
    # スペースの扱いを半角にすることで一時回避   
    #def spacing():
    #    output = keymap.InputTextCommand(" ")               
    #    output()
    #keymap_global["Space"] = spacing

    # 日付関連
    def inputdate():
        DATE_FORMAT = "%Y-%m%d"
        output = keymap.InputTextCommand(datetime.datetime.now().strftime(DATE_FORMAT))
        output()
    if crr_os == "win":
        keymap_global[ "Ctrl-Semicolon" ] = inputdate
    elif crr_os == "mac":
        keymap_global[ "Cmd-Semicolon" ] = inputdate 

    # ----------------------------------------
    #  定型文処理
    # ----------------------------------------

    def template_otsu():
        output = keymap.InputTextCommand("お疲れ様です。")
        output()
    keymap_global[ "User1-O" ] = template_otsu

    def template_syou():
        output = keymap.InputTextCommand("承知しました。")
        output()
    keymap_global[ "User1-S" ] = template_syou

    def template_yoro():
        output = keymap.InputTextCommand("以上、よろしくお願い致します。")
        output()
    keymap_global[ "User1-Y" ] = template_yoro

    # ----------------------------------------
    #  Coding
    # ----------------------------------------
    
    # Camel to Snake
    if 1:
        def Camel2Snake():
            line = getClipboardText()
            if len(line.splitlines(True)) == 1:
                snake = ""
                prev = ""
                for char in line:
                    if char.isdigit():
                        if prev.isalpha():
                            snake += "_"
                        snake += char
                    else :                                
                        if char.isupper():
                            snake += "_"
                            snake += char.lower()
                        else :
                            snake += char
                    prev = char
                output = keymap.InputTextCommand(snake)
                output() 
        keymap_global[ "User0-C" ] = keymap.defineMultiStrokeKeymap("User0-C")
        keymap_global[ "User0-C" ][ "User0-S" ] = Camel2Snake
    
    # DEC2HEX2BIN
    def dec2hex():
        line = getClipboardText()
        if len(line.splitlines(True)) == 1:
            dec = int(line)
            strhex = hex(dec)
            output = keymap.InputTextCommand(strhex)
            output() 
    keymap_global[ "User0-D" ] = dec2hex

 # language detection
    if 0:
        def get_language():
            try:
                curr = keymap.getTopLevelWindow()
                filename = curr.getText().split(" - ")
                filetype = filename[-2].split(".")
                return filetype[1]
            except IndexError:
                print("対象のファイルではないため処理をスキップします") 
                return False
 ##---------------------
 ##  Comment
 ##---------------------
        def ins_cmt():
            type = get_language()
            print(type)
            if type:
                if type == "md":
                    return "#"
                elif type == "py":
                    output = keymap.InputTextCommand("#")
                    output()
                elif type == "c":
                    output = keymap.InputTextCommand(r"/*  */")
                    output()
                    left = keymap.InputKeyCommand("Left","Left","Left")
                    left()
        keymap_global[ "User0-C" ] = keymap.defineMultiStrokeKeymap("User0-C")
        keymap_global[ "User0-C" ][ "User0-M" ] = ins_cmt

    # ----------------------------------------
    #  Misc.
    # ----------------------------------------

    # Customizing clipboard history list
    # Enable clipboard monitoring hook (Default:Enabled)
    keymap.clipboard_history.enableHook(True)

    # Maximum number of clipboard history (Default:1000)
    keymap.clipboard_history.maxnum = 10

    # Total maximum size of clipboard history (Default:10MB)
    keymap.clipboard_history.quota = 1*1024*1024

    # Fixed phrases
    json_path = ckit.ckit_misc.getProfilePath()+r"\AppData\Roaming\Keyhac\acnt.json"
    if os.path.exists(json_path):
        f = open(json_path, 'r')

        fixed_items = list(json.load(f).items())
    else:
        fixed_items = ["   None    "]
    # Disable keyhac
    def disable_keyhac():
        keymap.enableHook(False)
    # Menu item list
    other_items = [
        ( "Edit config.py",             keymap.command_EditConfig ),
        ( "Reload config.py",           keymap.command_ReloadConfig ),
        ( "Disable keyhac",             disable_keyhac               ),
    ]

    # Clipboard history list extenzsions
    keymap.cblisters += [
        ( "Pass", cblister_FixedPhrase(fixed_items) ),
        ( "Others", cblister_FixedPhrase(other_items) ),
    ]

    elapsed_time = time.time() - start
    print ("elapsed_time:{}".format(elapsed_time) + "[sec]")