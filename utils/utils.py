import re
import requests
from bs4 import BeautifulSoup
import time


def char_type_detect(texts):
    # korean
    if re.search(r"[\uac00-\ud7a3]", texts):
        return "ko"
    # japanese
    if re.search(r"[\u3040-\u30ff]", texts):
        return "jp"
    if re.search(r"[\u3190-\u319f]", texts):
        return "jp"
    # chinese
    if re.search(r"[\u2e80-\u2fd5]", texts):
        return "zh"
    if re.search(r"[\u3400-\u4dbf]", texts):
        return "zh"
    if re.search(r"[\u4e00-\u9FFF]", texts):
        return "zh"
    if re.search(r"[\uf900-\ufaad]", texts):
        return "zh"
    if re.search(r'[a-zA-Z]', texts):
        return 'en'
    return 'other'

def test_throughput(kw):
    nr_send = 0
    start_timer = time.time()
    while True:
        # 1 per second
        try:
            ret = search_kw(kw)
            nr_send += 1
#            time.sleep(2)
            print(ret)
        except Exception as e:
            if (len(e.args) > 0 and e.args[0] == 'Service is blocked'):
                now = time.time()
                print("Send {} in {} seconds ({} rps)".format(nr_send, now-start_timer, nr_send/(now-start_timer)))
                print(e.args[0], ": wait for 6 minutes")
                time.sleep(6 * 60)
                nr_send = 0
                start_timer = time.time()
            else:
                raise

def search_kw(kw, retry=False, callback=None, response_log=None):
    # "word", "char" "from" "explain"
    ret = {"word":kw}
    char_type = char_type_detect(kw)
    ret["char"] = char_type
    if char_type  != 'ko':
        return ret

    # let's do a translation for Korean word
    retry_time = 65 * 60
    nr_retry = 1
    r = ""
    while True:
        url="https://dict.naver.com/search.nhn?dicQuery={}".format(kw)
        r = requests.post(url, timeout=5)
        if response_log:
            response_log.write("{}\n".format({"url":url, "response":r.text}))
        if (r.text.find('Service access is temporarily blocked') != -1):
            if retry == False:
                raise Exception("Service is blocked")
            else:
            # give a retry
                print("{} Retry: Sleep for {} seconds".format(nr_retry, retry_time))
                print("Invoke call back before sleep")
                if callback:
                    callback()
                time.sleep(retry_time)
                nr_retry += 1
                continue;
        else:
            break;
    s = BeautifulSoup(r.text, 'lxml')
    ur = s.find('span',{'class':'c_b'})
    if ur:
        trans_word = ur.text
        trans_type = char_type_detect(trans_word)
        ret["explain"] = trans_word
        if trans_type == 'en':
            ret["from"] = "en"
        if trans_type == "ko":
            word_class2_span = s.find('span',{'class':'word_class2'})
            if (word_class2_span):
                annotate_word = word_class2_span.text.strip('(').strip(')')
                annotate_type = char_type_detect(annotate_word)
                if annotate_type == 'zh':
                    ret["from"] = 'zh'
                    ret["from_word"] = annotate_word
    return ret

