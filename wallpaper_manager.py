########################################################
#     Wallpaper Manager with wallhaven.cc integration  #
#                                                      #
#                  Author - Mato098                    #
#                                                      #
#                  Dated - Sept 2022                   #
########################################################


import json
import random
import sys
import tkinter as tk
import tkinter.messagebox

import os, re, time, subprocess
import downloader
import cleanup
from difPy import dif


def load_settings():
    key = ''
    pth = ''
    with open(os.path.join(path_auto(), 'settings.json'), 'r') as f:
        data = json.load(f)
        key = data['api_key']
        pth = data['download_directory']
    set_key(key)
    set_pth(pth)


def set_key(key: str):
    downloader.APIKEY = key
    global APIKEY
    global PTH
    APIKEY = key
    f = open(os.path.join(path_auto(), 'settings.json'), 'r')
    data = json.load(f)
    data['api_key'] = key
    f.close()
    f = open(os.path.join(path_auto(), 'settings.json'), 'w')
    json.dump(data, f)
    f.close()
    global apikey_l
    try:
        apikey_l.config(text=f'Your API key: {APIKEY}')
    except:
        pass


def set_pth(path: str):
    downloader.PTH = path
    global PTH
    PTH = path
    f = open(os.path.join(path_auto(), 'settings.json'), 'r')
    data = json.load(f)
    data['download_directory'] = path
    f.close()
    f = open(os.path.join(path_auto(), 'settings.json'), 'w')
    json.dump(data, f)
    f.close()
    global path_l
    try:
        path_l.config(text=f'Path to download directory: {PTH}')
    except:
        pass

def path_auto():
    filepth_lst = re.split('\\\\', os.path.realpath(__file__))
    filepth_lst.insert(1, os.sep)
    PTH = os.path.join(*filepth_lst[:-1])
    return PTH


def get_text_and_run(text, func):
    def text_exit():
        text = txt.get()
        _window.destroy()
        func(text)

    def text_exit_ev(event):
        text_exit()

    _window = tk.Tk()
    _window.title('Paste here')

    a = tk.Label(_window, text=text)
    a.grid(column=0, row=0)

    txt = tk.Entry(_window, width=80)
    txt.grid(column=0, row=1)
    txt.focus_force()

    button = tk.Button(_window, text='OK', command=text_exit)
    button.grid(row=2)
    _window.bind('<Return>', text_exit_ev)


def download_link():
    get_text_and_run("Made for wallhaven.cc, will not work for other sites", downloader.download_link)
    #time.sleep(1)
    #cleanup.cleanup(PTH)


def download_api():
    downloader.main()
    time.sleep(2)
    cleanup.cleanup(PTH)


def edit_api_key():
    get_text_and_run("Paste your key here:", set_key)


def cycle_wallpaper(given_name=''):
    name = get_wallpaper_name()
    curr_num = int(re.sub("[^0-9]", "", str(name)))
    filepth_lst = re.split('\\\\', os.path.realpath(__file__))
    filepth_lst.insert(1, os.sep)
    global PTH

    a = '''function Set-Wallpaper($MyWallpaper){
$code = @' 
using System.Runtime.InteropServices; 
namespace Win32{ 
    
     public class Wallpaper{ 
        [DllImport("user32.dll", CharSet=CharSet.Auto)] 
         static extern int SystemParametersInfo (int uAction , int uParam , string lpvParam , int fuWinIni) ; 
         
         public static void SetWallpaper(string thePath){ 
            SystemParametersInfo(20,0,thePath,3); 
         }
    }
 } 
'@

add-type $code 
[Win32.Wallpaper]::SetWallpaper($MyWallpaper)
}'''
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if given_name != '':
        if os.path.exists(f'{PTH}\\{given_name}.png'):
            subprocess.Popen(['powershell.exe', f'{a}; Set-Wallpaper(\"{PTH}\\{given_name}.png\")'],
                             startupinfo=startupinfo)
        else:
            subprocess.Popen(['powershell.exe', f'{a}; Set-Wallpaper(\"{PTH}\\{given_name}.jpg\")'],
                             startupinfo=startupinfo)
    else:
        for i in range(3):
            if os.path.exists(f'{PTH}\\{curr_num + 1}.png'):
                subprocess.Popen(['powershell.exe', f'{a}; Set-Wallpaper(\"{PTH}\\{curr_num + 1}.png\")'],
                                 startupinfo=startupinfo)
                break
            elif os.path.exists(f'{PTH}\\{curr_num + 1}.jpg'):
                subprocess.Popen(['powershell.exe', f'{a}; Set-Wallpaper(\"{PTH}\\{curr_num + 1}.jpg\")'],
                                 startupinfo=startupinfo)
                break
            elif i < 1:
                cleanup.cleanup(PTH)
                continue
            if i == 1:
                curr_num = 0
                print('going back to 1')
    time.sleep(0.5)
    try:
        update_curr_wallpaper_label()
    except:
        pass


def get_wallpaper_name():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    process = subprocess.Popen(["powershell.exe",
                                "Split-Path (Get-ItemProperty -Path \"HKCU:\Control Panel\Desktop\" -Name Wallpaper).Wallpaper -Leaf"],
                               stdout=subprocess.PIPE, startupinfo=startupinfo)

    out, err = process.communicate()
    return out


def delete_wallpaper():
    name = get_wallpaper_name()
    curr_num = int(re.sub("[^0-9]", "", str(name)))
    cycle_wallpaper()
    os.popen(f'cd {PTH} && DEL {curr_num}.*')
    update_curr_wallpaper_label()


def set_random_wallpaper():
    dirlist = os.listdir(PTH)
    a = str(random.randint(1, len(dirlist)))
    print(a)
    cycle_wallpaper(a)


def update_curr_wallpaper_label():
    name = get_wallpaper_name()
    curr_num = re.sub("[^0-9.jpg]", "", str(name))
    if curr_num[-3:] == '.pg':
        curr_num = curr_num[:-3] + '.png'
    global wallpap_name_l
    wallpap_name_l.config(text=f'Current wallpaper: {curr_num}')


def run_cleanup():
    cleanup.cleanup(PTH)


def edit_path():
    get_text_and_run('! Images will not be moved to new directory', set_pth)


def open_path():
    subprocess.Popen(['powershell.exe', f'explorer {PTH}'])


def delete_duplicates():  # TODO - terminal output
    a = dif(PTH, similarity="normal", px_size=50,
            show_progress=True, show_output=False, delete=True, silent_del=True)
    time.sleep(1)
    cleanup.cleanup(PTH)


def clear_schedule():
    os.system('SchTasks /Delete /TN "Wallpaper_task" /f')


def schedule_hourly():
    global python_install_dir
    clear_schedule()
    os.system(f'SchTasks /Create /SC HOURLY /TN "Wallpaper_task" /TR "{python_install_dir} {os.path.abspath("schedule_worker.py")}" /ST {schedule_time_txt_var.get()}')


def schedule_daily():
    global python_install_dir
    clear_schedule()
    os.system(f'SchTasks /Create /SC DAILY /TN "Wallpaper_task" /TR "{python_install_dir} {os.path.abspath("schedule_worker.py")}" /ST {schedule_time_txt_var.get()}')


def schedule_weekly():
    global python_install_dir
    clear_schedule()
    os.system(f'SchTasks /Create /SC WEEKLY /TN "Wallpaper_task" /TR "{python_install_dir} {os.path.abspath("schedule_worker.py")}" /ST {schedule_time_txt_var.get()}')


APIKEY = ''
PTH = ''
python_install_dir = r'C:\Users\Martin\AppData\Local\Programs\Python\Python38\pythonw.exe'

wallpap_name_l = 0
path_l = 0
apikey_l = 0
schedule_time_txt_var = 0


def main():
    global wallpap_name_l
    global path_l
    global apikey_l
    global schedule_time_txt_var

    window = tk.Tk()

    window.title("Mato's Wallpaper Manager")
    window.geometry('600x250')

    download_l = tk.Label(window, text="Download")
    download_l.grid(column=0, row=0)

    link_b = tk.Button(window, text="Download via link", command=download_link)
    link_b.grid(column=0, row=1)

    download_api_b = tk.Button(window, text='Download via API', command=download_api)
    download_api_b.grid(column=0, row=2)

    manage_l = tk.Label(window, text='Sort files')
    manage_l.grid(column=1, row=0)
    cleanup_b = tk.Button(window, text='Run cleanup', command=run_cleanup)
    cleanup_b.grid(column=1, row=1)
    duplicates_b = tk.Button(window, text='Delete duplicates, cleanup', command=delete_duplicates)
    duplicates_b.grid(column=1, row=2)
    wallpap_name_l = tk.Label(window, text=f'Current wallpaper: ')
    wallpap_name_l.grid(column=2, row=0)
    cycle_b = tk.Button(window, text='Cycle wallpaper', command=cycle_wallpaper)
    cycle_b.grid(column=2, row=1)
    del_b = tk.Button(window, text='Delete current wallpaper', command=delete_wallpaper)
    del_b.grid(column=2, row=2)
    random_b = tk.Button(window, text='Set random wallpaper', command=set_random_wallpaper)
    random_b.grid(column=2, row=3)

    dud = tk.Label(window)
    dud.grid(column=0, row=5)

    path_l = tk.Label(window, text=f'Path to download directory: {PTH}')
    path_l.grid(column=0, row=6, columnspan=3)
    path_b = tk.Button(window, text='Edit path', command=edit_path)
    path_b.grid(column=0, row=7, columnspan=3)
    open_b = tk.Button(window, text='Open folder', command=open_path)
    open_b.grid(column=2, row=7)

    apikey_l = tk.Label(window, text=f'Your API key: {APIKEY}')
    apikey_l.grid(column=0, row=8, columnspan=3)
    edit_key_b = tk.Button(window, text='Edit API key', command=edit_api_key)
    edit_key_b.grid(column=0, row=9, columnspan=3)

    schedule_l = tk.Label(window, text=f'Set scheduled change')
    schedule_l.grid(column=3, row=0)
    schedule_h_b = tk.Button(window, text='Set hourly', command=schedule_hourly)
    schedule_h_b.grid(column=3, row=1)
    schedule_d_b = tk.Button(window, text='Set daily', command=schedule_daily)
    schedule_d_b.grid(column=3, row=2)
    schedule_w_b = tk.Button(window, text='Set weekly', command=schedule_weekly)
    schedule_w_b.grid(column=3, row=3)
    schedule_w_b = tk.Button(window, text='Clear schedule', command=clear_schedule)
    schedule_w_b.grid(column=3, row=4)

    schedule_time_txt_var = tk.StringVar()
    schedule_time_txt = tk.Entry(window, textvariable=schedule_time_txt_var)
    schedule_time_txt.insert(0, '18:00')
    schedule_time_txt_var.set('18:00')
    schedule_time_txt.grid(column=3, row=5)



    load_settings()
    update_curr_wallpaper_label()

    window.mainloop()


if __name__ == "__main__":
    main()

