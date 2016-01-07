from bs4 import BeautifulSoup
import re

def parse_unescape(s):
    s = s.replace('\\t', '\t')
    s = s.replace('\\n', '\n')
    s = s.replace('\\r', '\r')
    s = s.replace('\\"', '"')
    s = s.replace('\\/', '/')
    s = re.sub('.*"html":"', '', s)
    return s[:-13]

def parse_cardwrap(feed):
    count = 0
    for d in feed.find_all('div', attrs={'class':'WB_cardwrap', 'action-type':'feed_list_item'}):
        print('-'*50)
        try:
            mid = d['mid']
            rid = d['mrid'][4:]
            detail = d.find('div', attrs={'class':'WB_feed_detail'}).find('div', attrs={'class':'WB_detail'})
            info = detail.find('div', attrs={'class':'WB_info'})
            userid = info.find('a')['usercard'][3:]
            username = info.find('a')['nick-name']
            mfrom = detail.find('div', attrs={'class':'WB_from'})
            date = mfrom.find('a')['date']
            text = detail.find('div', attrs={'class':'WB_text'})
            handle = d.find('div', attrs={'class':'WB_feed_handle'}).find('div', attrs={'class':'WB_handle'})
            forward = handle.find('span', attrs={'node-type':'forward_btn_text'})
            forward = forward.get_text().strip()[3:]
            comment = handle.find('span', attrs={'node-type':'comment_btn_text'})
            comment = comment.get_text().strip()[3:]
            like = handle.find('span', attrs={'node-type':'like_status'})
            like = like.get_text().strip()

            print('mid:', mid, 'userid:', userid, 'name:', username)
            print('date:', date, 'forward:', forward, 'comment:', comment, 'like:', like)
            print(text.get_text().encode('utf8', 'ignore').decode('utf8'))
            count += 1
        except (KeyError, AttributeError) as e:
            continue
    return count

def parse_html(s):
    feed = ''
    for l in s.split('\n'):
        if 'pl.content.homefeed.index' in l or 'pl_unlogin_home_feed' in l:
            feed += parse_unescape(l)

    feed = BeautifulSoup(feed, 'html.parser')
    return parse_cardwrap(feed)

def parse_ajax(s):
    return parse_cardwrap(BeautifulSoup(parse_unescape(s), 'html.parser'))
