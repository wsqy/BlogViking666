from django import template
register = template.Library()

word_in = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890,.-"


@register.filter
def zh_truncatewords(ss, num=10, end_text='...'):
    out = []
    tmp_word = []
    # 将字符串转换为list
    ss_list = list(ss)
    for i in ss_list:
        # 如果长度达到要求就可以退出了
        if len(out) >= num:
            out.append(end_text)
            break
        # 如果字符满足形成一个单词的元素就将他存在tmp_word里
        if i in word_in:
            tmp_word.append(i)
        else:
            # 如果tmp_word非空 那说明成功匹配一个单词，加进去的同时记得清空tmp_word
            if tmp_word:
                out.append(''.join(tmp_word))
                tmp_word = []
            # 不管tmp_word怎样，没匹配单词 就说明是汉子空格等清空，照样算匹配一个单词
            out.append(i)

    out_str = ''.join(out)
    return out_str


@register.filter
def category_filter(querySets, subId=None):
    # query = [queryset for queryset in querySets if queryset.SubClass_id == subId]
    # return query
    return querySets.filter(SubClass=subId)

@register.filter
def urlparse_filter(url):
    bb = url.split('/')
    return "%s//%s/" % (bb[0], bb[2])
