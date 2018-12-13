# coding=utf-8
import time
import csv

import os
import wx
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import argparse


def generate_title(title):
    return '''
        <section class="" style="max-width: 100%%ds;overflow: hidden;font-family: Arial;border-width: 0px;border-style: none;border-color: initial;color: rgb(49, 147, 105);box-sizing: border-box !important;word-wrap: break-word !important;">
            <section style="margin-top: 5px;margin-bottom: 5px;max-width: 100%%;clear: both;border-width: 0px;border-style: none;border-color: initial;box-sizing: border-box !important;word-wrap: break-word !important;">
                <section style="max-width: 100%%;box-sizing: border-box;border-top-width: 2.5px;border-top-style: solid;border-color: rgb(239, 112, 96);font-size: 1em;font-weight: inherit;text-decoration: inherit;color: rgb(255, 255, 255);word-wrap: break-word !important;">
                    <section style="margin-top: 2px;max-width: 100%%;border-width: 0px;border-style: initial;border-color: rgb(239, 112, 96);overflow: hidden;color: inherit;box-sizing: border-box !important;word-wrap: break-word !important;">
                        <section style="max-width: 100%%;display: inline-block;font-size: 1em;font-family: inherit;font-weight: inherit;text-align: inherit;text-decoration: inherit;color: inherit;border-color: rgb(239, 112, 96);box-sizing: border-box !important;word-wrap: break-word !important;">
                            <section style="padding: 5px 10px;max-width: 100%%;display: inline-block;line-height: 1.4em;height: 32px;vertical-align: top;font-family: inherit;font-weight: bold;float: left;color: inherit;border-color: rgb(212, 43, 21);box-sizing: border-box !important;word-wrap: break-word !important;background: rgb(239, 112, 96);">%s</section>
                            <section style="max-width: 100%%;display: inline-block;vertical-align: top;width: 0px;height: 0px;border-top-width: 32px;border-top-style: solid;border-top-color: rgb(239, 112, 96);border-right-width: 32px;border-right-style: solid;border-right-color: transparent;border-top-right-radius: 4px;border-bottom-left-radius: 2px;color: inherit;box-sizing: border-box !important;word-wrap: break-word !important;">
                            </section>
                        </section>
                    </section>
                </section>
            </section>
        </section>
    ''' % title


def generate_br():
    return '''
        <p style="max-width: 100%%;min-height: 1em;box-sizing: border-box !important;word-wrap: break-word !important;">
            <span style="max-width: 100%%;font-size: 15px;color: rgb(136, 136, 136);box-sizing: border-box !important;word-wrap: break-word !important;">
                <br>
            </span>
        </p>
    '''


def generate_celebrity(celebrity):
    print celebrity
    return '''
        <section class="" data-tools-id="14859" style="margin-top: 20px;max-width: 100%%;overflow: hidden;box-sizing: border-box !important;word-wrap: break-word !important;">
            <p style="margin-right: auto;margin-left: auto;padding: 8px;max-width: 100%%;min-height: 1em;border-width: 1px;border-style: solid;border-color: rgb(109, 116, 139);border-radius: 100%%;overflow: hidden;width: 209.46px;box-sizing: border-box !important;word-wrap: break-word !important;">
                <img class="" data-copyright="0" data-cropselx1="0" data-cropselx2="189" data-cropsely1="0" data-cropsely2="191" data-ratio="0.9911111111111112" src="https://mmbiz.qpic.cn/mmbiz_png/y8hNw6oWsicEsWfYYfz8Gmia7v1wOVOHre8pNfURhvRQXnribfjZ6g6C3TzfYP0ZoRfPqzzndg0xCT0rcUQs0e9Zw/640?wx_fmt=png" data-type="png" data-w="225" style="border-width: 1px;border-style: solid;border-color: rgb(238, 237, 235);border-radius: 100%%;vertical-align: top;background-color: rgb(238, 237, 235);background-size: 22px;background-position: 50%% 50%%;background-repeat: no-repeat;height: 191px;box-sizing: border-box !important;word-wrap: break-word !important;width: 193px;">
            </p>
            <p style="max-width: 100%%;min-height: 1em;text-align: center;box-sizing: border-box !important;word-wrap: break-word !important;">
                <br style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">
            </p>
            <p style="max-width: 100%%;min-height: 1em;text-align: center;box-sizing: border-box !important;word-wrap: break-word !important;">
                <span style="max-width: 100%%;color: rgb(119, 119, 119);box-sizing: border-box !important;word-wrap: break-word !important;">
                    <strong style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">%s</strong>
                </span>
            </p>
            <p style="max-width: 100%%;min-height: 1em;text-align: center;box-sizing: border-box !important;word-wrap: break-word !important;">
                <span style="max-width: 100%%;color: rgb(119, 119, 119);box-sizing: border-box !important;word-wrap: break-word !important;">
                    <strong style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">%s</strong>
                </span>
            </p>
            <section style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">
                <p style="max-width: 100%%;min-height: 1em;box-sizing: border-box !important;word-wrap: break-word !important;">
                    <span style="max-width: 100%%;font-size: 15px;color: rgb(136, 136, 136);box-sizing: border-box !important;word-wrap: break-word !important;">%s</span>
                </p>
            </section>
        </section>
    ''' % (celebrity["name"], celebrity["title"], celebrity["introduction"])


def generate_movie(movie):
    print movie
    if "title" in movie and movie["title"].replace(" ", "") != "":
        movie["title"] = '''
            <p style="max-width: 100%%;min-height: 1em;text-align: center;box-sizing: border-box !important;word-wrap: break-word !important;">
                <span style="max-width: 100%%;color: rgb(119, 119, 119);box-sizing: border-box !important;word-wrap: break-word !important;">
                    <strong style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">%s</strong>
                </span>
            </p>
        ''' % movie["title"]
    else:
        movie["title"] = ""
    return '''
            <section class="" data-tools-id="14859" style="margin-top: 20px;max-width: 100%%;overflow: hidden;box-sizing: border-box !important;word-wrap: break-word !important;">
                <p style="margin-right: auto;margin-left: auto;padding: 8px;max-width: 100%%;min-height: 1em;border-width: 1px;border-style: solid;border-color: rgb(109, 116, 139);border-radius: 100%%;overflow: hidden;width: 209.46px;box-sizing: border-box !important;word-wrap: break-word !important;">
                    <img class="" data-copyright="0" data-cropselx1="0" data-cropselx2="189" data-cropsely1="0" data-cropsely2="191" data-ratio="0.9911111111111112" src="https://mmbiz.qpic.cn/mmbiz_png/y8hNw6oWsicEsWfYYfz8Gmia7v1wOVOHre8pNfURhvRQXnribfjZ6g6C3TzfYP0ZoRfPqzzndg0xCT0rcUQs0e9Zw/640?wx_fmt=png" data-type="png" data-w="225" style="border-width: 1px;border-style: solid;border-color: rgb(238, 237, 235);border-radius: 100%%;vertical-align: top;background-color: rgb(238, 237, 235);background-size: 22px;background-position: 50%% 50%%;background-repeat: no-repeat;height: 191px;box-sizing: border-box !important;word-wrap: break-word !important;width: 193px;">
                </p>
                <p style="max-width: 100%%;min-height: 1em;text-align: center;box-sizing: border-box !important;word-wrap: break-word !important;">
                    <br style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">
                </p>
                <p style="max-width: 100%%;min-height: 1em;text-align: center;box-sizing: border-box !important;word-wrap: break-word !important;">
                    <span style="max-width: 100%%;color: rgb(119, 119, 119);box-sizing: border-box !important;word-wrap: break-word !important;">
                        <strong style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">%s</strong>
                    </span>
                </p>
                <p style="max-width: 100%%;min-height: 1em;text-align: center;box-sizing: border-box !important;word-wrap: break-word !important;">
                    <span style="max-width: 100%%;color: rgb(119, 119, 119);box-sizing: border-box !important;word-wrap: break-word !important;">
                        <strong style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">%s</strong>
                    </span>
                </p>
                <p style="max-width: 100%%;min-height: 1em;text-align: center;box-sizing: border-box !important;word-wrap: break-word !important;">
                    <span style="max-width: 100%%;color: rgb(119, 119, 119);box-sizing: border-box !important;word-wrap: break-word !important;">
                        <strong style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">%s</strong>
                    </span>
                </p>
                %s
                <section style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">
                    <p style="max-width: 100%%;min-height: 1em;box-sizing: border-box !important;word-wrap: break-word !important;">
                        <span style="max-width: 100%%;font-size: 15px;color: rgb(136, 136, 136);box-sizing: border-box !important;word-wrap: break-word !important;">%s</span>
                    </p>
                </section>
            </section>
        ''' % (movie["name"], movie["date"], movie["genre"], movie["title"], movie["introduction"])


def generate_full(celebrity_list, movie_list):
    result = []
    for i in range(5):
        result.append(generate_br())
    result.append(generate_title("本期焦点"))
    for i in range(10):
        result.append(generate_br())
    result.append(generate_title("人物"))
    for celebrity in celebrity_list:
        result.append(generate_br())
        result.append(generate_br())
        result.append(generate_celebrity(celebrity))
    result.append(generate_br())
    result.append(generate_br())
    if movie_list is not None:
        result.append(generate_title("作品"))
        for movie in movie_list:
            result.append(generate_br())
            result.append(generate_br())
            result.append(generate_movie(movie))
    return [item.replace("\n", "").replace("%%", "%").strip() for item in result]




# option = webdriver.ChromeOptions()
# option.add_argument(
#     "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36")
# browser = webdriver.Chrome(options = option,
#                            executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
#
# browser.get('http://mp.weixin.qq.com')


class my_frame(wx.Frame):
    """We simple derive a new class of Frame"""

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (350, 180))
        panel = wx.Panel(self, -1)
        self.celebrity_button = wx.Button(panel, -1, "选择人物档案", pos = (50, 20))
        self.movie_button = wx.Button(panel, -1, "选择作品档案", pos = (200, 20))
        self.flush_button = wx.Button(panel, -1, "确认刷入", pos = (120, 80))
        self.Bind(wx.EVT_BUTTON, self.open_celebrity_selector, self.celebrity_button)
        self.Bind(wx.EVT_BUTTON, self.open_movie_selector, self.movie_button)
        self.Bind(wx.EVT_BUTTON, self.flush_data, self.flush_button)
        self.celebrity_button.SetDefault()
        self.movie_button.SetDefault()
        self.celebrity_path = None
        self.movie_path = None

    def open_celebrity_selector(self, event):
        dialog = wx.FileDialog(self, "Open file...", os.getcwd(), wildcard = "*.csv")
        if dialog.ShowModal() == wx.ID_OK:
            self.celebrity_path = dialog.GetPath()
        dialog.Destroy()

    def open_movie_selector(self, event):
        dialog = wx.FileDialog(self, "Open file...", os.getcwd(), wildcard = "*.csv")
        if dialog.ShowModal() == wx.ID_OK:
            self.movie_path = dialog.GetPath()
        dialog.Destroy()

    def flush_data(self, event):
        try:
            with open(self.celebrity_path, 'r') as csvfile:
                fieldnames = ["name", "title", "introduction"]
                reader = csv.DictReader(csvfile, fieldnames = fieldnames)
                next(reader)
                celebrity_list = [item for item in reader]
                csvfile.close()

            # with open(self.movie_path, 'r') as csvfile:
            #     fieldnames = ["name", "title", "genre", "date", "introduction"]
            #     reader = csv.DictReader(csvfile, fieldnames = fieldnames)
            #     next(reader)
            #     movie_list = [item for item in reader]
            #     csvfile.close()

            with open("result.txt", "wb") as f:
                import re
                f.write(re.sub("> +<", "><", "".join(generate_full(celebrity_list = celebrity_list, movie_list = None)).replace("\t", "")))

            #
            # if browser.current_url.find("t=media/appmsg_edit&action=edit") == -1 and browser.current_url.find("t=media/appmsg_edit_v2&action=edit") == -1:
            #     return wx.MessageBox('您不在编辑页面上！', '错误', wx.OK | wx.ICON_INFORMATION)
            #
            # script = '''
            #     var article_container = $($("iframe#ueditor_0")[0].contentWindow.document).children("html").children("body");
            #     var article = null;
            #     article_container.empty();
            # '''
            #
            # for item in generate_full(celebrity_list = celebrity_list, movie_list = movie_list):
            #     script += '''
            #         article = '%s';
            #         article_container.append($(article));
            #     ''' % item
            #
            #     # print '''
            #     #     article = '%s;
            #     #     article_container.append($(article));
            #     # ''' % item
            #
            # browser.execute_script(script)

        except Exception,e:
            print e
            wx.MessageBox('请提供有效的csv文件！', '错误', wx.OK | wx.ICON_INFORMATION)


app = wx.App(False)
frame = my_frame(None, '幻历周刊生成器')
frame.Show()
app.MainLoop()
