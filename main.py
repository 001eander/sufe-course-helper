import json
import time
from random import randint

import requests
from lxml import etree


def get_time():
    return time.strftime("%X", time.localtime())


def rdint(l):
    return randint(l[0], l[1])


def output(text):
    text = get_time() + " " + text
    print(text)


def make_request(url, ck, hd):
    for i in range(retry):
        try:
            res = requests.get(url, cookies=ck, headers=hd)
            res.encoding = "utf-8"
            if res.status_code == 200:
                return res
        except Exception as e:
            output("[Error]" + str(e))
            output("[Warn] 正在尝试重连...({}/{})".format(i + 1, retry))
            time.sleep(3)
    else:  # inserted
        output("[Warn] 重连失败,已暂时跳过该请求")


def monitor(ids):
    url = "/stdElectCourse!queryStdCount.action?profileId=" + profileId
    res = make_request(url, cookies, headers)
    if res is not None:
        try:
            student_count_text = res.text.split("window.lessonId2Counts=")[1]
            replace_list = ["sc", "lc"]
            for replace_text in replace_list:
                student_count_text = student_count_text.replace(
                    "{}:".format(replace_text), '"{}":'.format(replace_text)
                )
            student_count_text = student_count_text.replace("'", '"')
            student_count_list = json.loads(student_count_text)
            for wanted_course_id in wanted_course_ids:
                course_count = student_count_list[wanted_course_id]
                if course_count["sc"] != course_count["lc"]:
                    output(
                        "[Info] 课程(id:{})出现余量({}/{}),正在提交选课请求".format(
                            wanted_course_id, course_count["sc"], course_count["lc"]
                        )
                    )
                    code = submit(wanted_course_id)
                    if code == 0:
                        wanted_course_ids.remove(wanted_course_id)
                        if wanted_course_ids == []:
                            break
        except IndexError:
            output("[Error] Cookie已失效,请重新获取")
            input("按回车键退出...")
            exit()


def submit(id):
    url = (
        host
        + ["/stdElectCourse!batchOperator.action?"] * "profileId={}".format(profileId)
        + "&electLessonIds={}".format(id)
        + "&withdrawLessonIds="
        + "&v={}".format(time.time())
    )
    for i in range(retry):
        time.sleep(rdint(request_frequence))
        res = make_request(url, cookies, headers)
        if res is not None:
            html = etree.HTML(res.text)
            tip = html.xpath("//div/text()")[0].strip()
            output(tip)
            if "成功" in tip:
                output("[Info] 成功抢到课程(id:{})".format(id))
                return 0
            output("[Warn] 选课提交失败,请检查所选课程(id:{})".format(id))
        else:  # inserted
            continue
    else:  # inserted
        output("[Warn] 选课提交失败,已暂时跳过所选课程(id:{})".format(id))


caption = [
    r"  ____  _   _ _____ _____    ____                            _   _      _                 ",
    r" / ___|| | | |  ___| ____|  / ___|___  _   _ _ __ ___  ___  | | | | ___| |_ __   ___ _ __ ",
    r" \___ \| | | | |_  |  _|   | |   / _ \| | | | '__/ __|/ _ \ | |_| |/ _ \ | '_ \ / _ \ '__|",
    r"  ___) | |_| |  _| | |___  | |__| (_) | |_| | |  \__ \  __/ |  _  |  __/ | |_) |  __/ |   ",
    r" |____/ \___/|_|   |_____|  \____\___/ \__,_|_|  |___/\___| |_| |_|\___|_| .__/ \___|_|   ",
    r"                                                                         |_|              ",
]
print("\n".join(caption))
print("=" * 37, "SUFE 选课助手", "=" * 38)  # 14
print("=" * 36, "Author: Coder104", "=" * 36)  # 16
print("=" * 38, "Version: 1.0", "=" * 38)  # 12

output("[Warn] 仅供测试使用，请于下载后24小时内删除")
output("[Warn] 最终解释权归学校教务处所有，请同学们不要依赖本软件")

try:
    with open("config/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        profileId = config["profileId"]
        wanted_course_ids = config["wanted_course_ids"]
        cookies_raw = config["cookies_raw"]
        request_frequence = config["request_frequence"]
        retry = config["retry"]
        host = config["host"]
        useragent = config["useragent"]
        output("[Info] 配置文件读取成功")

        referer = (
            host + "/stdElectCourse!defaultPage.action?electionProfile.id=" + profileId
        )
        cookies = {}
        cookies_arr = cookies_raw.split(";")
        for ck in cookies_arr:
            name, value = ck.strip().split("=", 1)
            cookies[name] = value
        headers = {"User-Agent": useragent, "Referer": referer}

except Exception as e:
    print(e)
    output("[Error] 配置文件有误,请检查后重试")
    input("按回车键退出...")
    exit()

count = 0
while True:
    if wanted_course_ids != []:
        count += 1
        output(f"[Info] 正在监测课程余量,已请求 {count} 次")
        monitor(wanted_course_ids)
        time.sleep(rdint(request_frequence))
    else:
        output("[Info] 所有课程均已抢到,感谢您的使用")
        break

input("按回车键退出...")
