#--*--coding:utf-8--*--

import urllib.request
import regex as re
import datetime

class Spider():
    def main(self,url_row):
        start_time = datetime.datetime.now()
        joke_list = []
        for page in range(1,11):
            url = url_row + str(page+1) +'/'
            resources = self.download(url)
            blocks = self.get_block(resources)
            jokes = self.cont_parser(str(blocks))
            for block in blocks:
                jokes = self.cont_parser(str(block))
                joke_list.append(jokes)
        self.output(joke_list)
        end_time = datetime.datetime.now()
        print('\n\n\n\n本次执行共耗时%s'%(end_time-start_time))

    def download(self, url):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
        if url is None:
            return None
        gethtml = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(gethtml)
        if response.getcode() != 200:
            return None
        return response.read().decode('utf-8')

    def get_block(self,resources):
        block = []
        pattern = re.compile(r'((div class="article block untagged mb15" id=\'qiushi_tag_\d+)(.|\n)*?(<div class="single-clear">))')
        block = re.findall(pattern, resources)
        return block
		
    def cont_parser(self,resources):
        joke_info = []
        author = re.compile(r'((?<=<h2>).*?(?=</h2>))')
        like = re.compile(r'((?<=<span class="stats-vote"><i class="number">)\d+(?=</i>))')
        comment = re.compile(r'((?<=<i class="number">)\d+(?=</i> 评论))')
        content = re.compile(r'((?<=<div class="content">(.|\n)*?<span>).*?(?=</span>))')
        try:
            joke_info.append(re.findall(author, resources)[0])
        except:
            joke_info.append('')
        try:
            joke_info.append(re.findall(content, resources)[0][0])
        except:
            joke_info.append('')
        try:
            joke_info.append(re.findall(like, resources)[0])
        except:
            joke_info.append('')
        try:
            joke_info.append(re.findall(comment, resources)[0])
        except:
            joke_info.append('')

        return joke_info

    def output(self,jokes):
        # print(jokes)
        with open('spider.txt','w') as f:
            for joke in jokes:
                # print(joke)
                try:
                    f.write(joke[0] + ':' + joke[1] + '\n')
                except:
                    print('step1 输出失败')
                try:
                    f.write(joke[2]+'人喜欢    '+joke[3]+'条评论'+'\n')
                except:
                    print('step2输出失败')

        f.close()
        return
if __name__=='__main__':
    url = 'http://www.qiushibaike.com/text/page/'
    qiubai = Spider()
    qiubai.main(url)