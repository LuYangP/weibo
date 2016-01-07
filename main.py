from login import login
from parse import parse_html, parse_ajax
import requests
import sys
import cons
import re

def main():
    LOGIN = True
    username = sys.argv[1]
    password = sys.argv[2]

    s = requests.Session()
    if LOGIN:
        s.cookies = login(username, password)
    else:
        r = s.get(cons.VISITOR_INCARNATE)

    r = s.get(cons.WEIBO_MAIN)
    r = r.content.decode('utf8')
    uid = re.search("\$CONFIG\['uid'\]='([0-9]+)';", r).group(1)
    count = 0
    for i in range(1, 11):
        r = s.get(cons.WEIBO_HOME_NUMPAGE.format(uid, i-1, i))
        print('PAGE:', i, 'HTML')
        count += parse_html(r.content.decode('utf8'))
        for j in range(0, 2):
            r = s.get(cons.WEIBO_HOME_AJAX.format(i, i, j))
            print('PAGE:', i, 'BAR:', j)
            count += parse_ajax(r.content.decode('unicode-escape'))
    print(count)

if __name__ == '__main__':
    main()
