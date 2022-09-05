########################################################
#        Program to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                                                      #
#                  Dated- 26 June 2016                 #
#                 Update - 11 June 2019                #
########################################################
import hashlib
import os
import requests
import urllib
import json
import re
import tkinter as tk
from tkinter import ttk

os.makedirs('Wallhaven', exist_ok=True)
BASEURL = ""
cookies = dict()

global APIKEY
global PTH

def download_link(link: str):
    if link[:4] != 'http':
        print('bad URL')
        return
    r = requests.get(link)
    print(r)
    code = r.content
    small_links = re.findall("small/[0-9a-z/]*\.jpg", str(code))
    print("found", len(small_links), "links")

    concat = ""
    for i in small_links:
        concat += i

    img_ids = re.findall("/[a-z0-9]*\.", concat)
    img_ids = list(map(lambda a: a[1:-1], img_ids))
    print(img_ids)

    for i in range(len(img_ids)):
        img_link = f'https://w.wallhaven.cc/full/{img_ids[i][0:2]}/wallhaven-{img_ids[i]}.jpg'
        os.popen(f'cd {PTH} && curl -O {img_link}')



def downloadPage(pageId, totalImage):
    url = BASEURL + str(pageId)
    print(url)
    urlreq = requests.get(url, cookies=cookies)
    pagesImages = json.loads(urlreq.content)
    pageData = pagesImages["data"]

    for i in range(len(pageData)):
        currentImage = (((pageId - 1) * 24) + (i + 1))

        url = pageData[i]["path"]

        filename = os.path.basename(url)
        osPath = os.path.join(PTH, filename)
        if not os.path.exists(osPath):
            imgreq = requests.get(url, cookies=cookies)
            if imgreq.status_code == 200:
                print("Downloading : %s - %s / %s" % (filename, currentImage, totalImage))
                with open(osPath, 'ab') as imageFile:
                    for chunk in imgreq.iter_content(1024):
                        imageFile.write(chunk)
            elif (imgreq.status_code != 403 and imgreq.status_code != 404):
                print("Unable to download %s - %s / %s" % (filename, currentImage, totalImage))
        else:
            print("%s already exist - %s / %s" % (filename, currentImage, totalImage))


def Image_md5hash(im_file):
    im = tk.Image.open(im_file)
    return hashlib.md5(im.tostring()).hexdigest()


def main():

    def get_3val_binary(args) -> str:#fst arg=1, second=10, third=100 -> 111
        num = ''
        for i in range(len(args)):
            num += ('1' if args[i].instate(['selected']) else '0')
        return num

    def parse_gui():
        sort_mode = 'views'
        for i in sort_lst:
            if i.instate(['selected']):
                sort_mode = i.cget('text')

        purity = get_3val_binary([sfw_c, sketchy_c, nsfw_c])
        categories = get_3val_binary([cat_general_c, cat_anime_c, cat_people_c])
        global BASEURL
        BASEURL = 'https://wallhaven.cc/api/v1/search?apikey='\
                  + APIKEY + '&topRange=' + sort_toplist_txt.get() + f'&atleast={resolution_txt_var.get()}&ratios={ratio_txt_var.get()}&order=desc&sorting={sort_mode}&purity={purity}&categories={categories}&page='
#
        pgid = int(pages_txt_var.get())
        totalImageToDownload = str(24 * pgid)
        print('Number of Wallpapers to Download: ' + totalImageToDownload)
        downloadoffset = int(pages_from_txt_var.get())

        for j in range(downloadoffset, downloadoffset + pgid):
            pass
            downloadPage(j, totalImageToDownload)

    window = tk.Tk()
    window.title("API downloader")
    window.geometry('300x290')
    window.focus_force()

    purity_l = tk.Label(window, text='Purity')
    purity_l.grid(column=0, row=0)
    sfw_c = ttk.Checkbutton(window, text='SFW')
    sfw_c.grid(column=0, row=1, sticky='W')
    sketchy_c = ttk.Checkbutton(window, text='Sketchy')
    sketchy_c.grid(column=0, row=2, sticky='W')
    nsfw_c = ttk.Checkbutton(window, text='NSFW')
    nsfw_c.grid(column=0, row=3, sticky='W')

    categories_l = tk.Label(window, text='Categories')
    categories_l.grid(column=0, row=5)
    cat_general_c = ttk.Checkbutton(window, text='General')
    cat_general_c.grid(column=0, row=6, sticky='W')
    cat_anime_c = ttk.Checkbutton(window, text='Anime')
    cat_anime_c.grid(column=0, row=7, sticky='W')
    cat_people_c = ttk.Checkbutton(window, text='People')
    cat_people_c.grid(column=0, row=8, sticky='W')

    resolution_l = tk.Label(window, text='Resolution(at least)')
    resolution_l.grid(column=1, row=0)
    resolution_txt_var = tk.StringVar()
    resolution_txt = tk.Entry(window, textvariable=resolution_txt_var)
    resolution_txt.insert(0, '1920x1080')
    resolution_txt_var.set('1920x1080')
    resolution_txt.grid(column=1, row=1)

    ratio_l = tk.Label(window, text='Ratio')
    ratio_l.grid(column=1, row=2)
    ratio_txt_var = tk.StringVar()
    ratio_txt = tk.Entry(window, textvariable=ratio_txt_var)
    ratio_txt.insert(0, '16x9')
    ratio_txt_var.set('16x9')
    ratio_txt.grid(column=1, row=3)

    sort_by_l = tk.Label(window, text='Sort by')
    sort_by_l.grid(column=2, row=0)
    sort_relevance_c = ttk.Checkbutton(window, text='relevance')
    sort_relevance_c.grid(column=2, row=1, sticky='W')
    sort_random_c = ttk.Checkbutton(window, text='random')
    sort_random_c.grid(column=2, row=2, sticky='W')
    sort_date_added_c = ttk.Checkbutton(window, text='date_added')
    sort_date_added_c.grid(column=2, row=3, sticky='W')
    sort_views_c = ttk.Checkbutton(window, text='views')
    sort_views_c.grid(column=2, row=4, sticky='W')
    sort_favorites_c = ttk.Checkbutton(window, text='favorites')
    sort_favorites_c.grid(column=2, row=5, sticky='W')
    sort_toplist_c = ttk.Checkbutton(window, text='toplist')
    sort_toplist_c.grid(column=2, row=6, sticky='W')
    toplist_txt_var = tk.StringVar()
    sort_toplist_txt = tk.Entry(window, textvariable=toplist_txt_var)
    sort_toplist_txt.insert(0, '1M')
    toplist_txt_var.set('1M')
    sort_toplist_txt.grid(column=1, row=6)
    sort_hot_c = ttk.Checkbutton(window, text='hot')
    sort_hot_c.grid(column=2, row=7, sticky='W')
    oo = tk.Label(window, text='Choose only one')
    oo.grid(column=2, row=8, sticky='W')

    pages_l = tk.Label(window, text='Pages to download')
    pages_l.grid(column=1, row=9, sticky='W')
    pages_txt_var = tk.StringVar()
    pages_txt = tk.Entry(window, textvariable=pages_txt_var)
    pages_txt.insert(0, '1')
    pages_txt_var.set('1')
    pages_txt.grid(column=2, row=9)
    pages_from_l = tk.Label(window, text='Start from page')
    pages_from_l.grid(column=1, row=10, sticky='W')
    pages_from_txt_var = tk.StringVar()
    pages_from_txt = tk.Entry(window, textvariable=pages_from_txt_var)
    pages_from_txt.insert(0, '1')
    pages_from_txt_var.set('1')
    pages_from_txt.grid(column=2, row=10)

    dummy = tk.Label(window)
    dummy.grid(column=0, row=11)

    download_b = tk.Button(window, text='Download', width=15, command=parse_gui)
    download_b.grid(columnspan=3, column=0, row=12)

    sort_lst = [sort_relevance_c, sort_random_c, sort_date_added_c, sort_views_c, sort_favorites_c, sort_toplist_c,
                sort_hot_c]
    for i in sort_lst:  # are by default half-checked...
        i.state(['!alternate'])
    for i in [sfw_c, sketchy_c, nsfw_c, cat_people_c, cat_anime_c, cat_general_c]:
        i.state(['!alternate'])
    sort_views_c.state(['selected'])
    cat_people_c.state(['selected'])
    cat_anime_c.state(['selected'])
    cat_general_c.state(['selected'])
    sfw_c.state(['selected'])

    tk.mainloop()


if __name__ == '__main__':
    main()
