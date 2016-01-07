from login import login
from parse import parse_html, parse_ajax
import requests
import sys
import cons

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
    count = 0
    for i in range(1, 11):
        #http://weibo.com/u/5821527146/home?end_id=3928401985213835&pre_page=1&page=2&pids=Pl_Content_HomeFeed&ajaxpagelet=1&ajaxpagelet_v6=1&__ref=/u/5821527146/home&_t=FM_145208753087823
        r = s.get(cons.WEIBO_HOME_NUMPAGE.format('5821527146', i-1, i))
        print('PAGE:', i, 'HTML')
        count += parse_html(r.content.decode('utf8'))
        for j in range(0, 2):
            #http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&from=feed&loc=nickname&is_all=1&pre_page=1&page=1&max_id=&end_id=3928391273502075&pagebar=0&filtered_min_id=&pl_name=Pl_Official_MyProfileFeed__25&id=1005053910587095&script_uri=/u/3910587095&feed_type=0&domain_op=100505&__rnd=1452088596216
            r = s.get(cons.WEIBO_HOME_AJAX.format(i-1, i, j))
            print('PAGE:', i, 'BAR:', j)
            count += parse_ajax(r.content.decode('unicode-escape'))
    print(count)


if __name__ == '__main__':
    # This is a test
    main()
