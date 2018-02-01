# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


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
    if "title" in movie:
        movie["title"] = '''
            <p style="max-width: 100%%;min-height: 1em;text-align: center;box-sizing: border-box !important;word-wrap: break-word !important;">
                <span style="max-width: 100%%;color: rgb(119, 119, 119);box-sizing: border-box !important;word-wrap: break-word !important;">
                    <strong style="max-width: 100%%;box-sizing: border-box !important;word-wrap: break-word !important;">%s</strong>
                </span>
            </p>
        '''
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
    result.append(generate_title("作品"))
    for movie in movie_list:
        result.append(generate_br())
        result.append(generate_br())
        result.append(generate_movie(movie))
    return [item.replace("\n", "").replace("%%", "%").strip() for item in result]


option = webdriver.ChromeOptions()
option.add_argument(
    "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36")
browser = webdriver.Chrome(options = option,
                           executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")

browser.get('http://mp.weixin.qq.com')


def passed(driver):
    print driver.current_url
    return driver.current_url.find("t=media/appmsg_edit&action=edit") != -1 or driver.current_url.find("t=media/appmsg_edit_v2&action=edit") != -1


WebDriverWait(driver = browser, timeout = 600).until(passed)

time.sleep(10)

script = '''
    var article_container = $($("iframe#ueditor_0")[0].contentWindow.document).children("html").children("body");
    var article = null; 
    article_container.empty();
'''

for item in generate_full(celebrity_list = [{"name": "汉斯·鲁道夫·吉格尔", "title": "异形造型师", "introduction": "瑞士艺术家汉斯·鲁道夫·吉格尔（Hans Rudolf Giger）出生于格劳宾登州库尔。吉格尔曾为《异形》（Alien）设计外星生物，并因此获得奥斯卡金像奖的最佳视觉效果奖。2013年，吉格尔被列入科幻与奇幻名人堂。"}], movie_list = []):
    script += '''
        article = '%s';
        article_container.append($(article));
    ''' % item

    print '''
        article = '%s;
        article_container.append($(article));
    ''' % item

browser.execute_script(script)

