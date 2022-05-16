#1 脏数据清洗，然后储存进数据库
#2 例子：1:...没有人才，怎么上得去？""我们向科学技术现代化进军，要有一支[浩浩荡荡]的工人阶级的又红又专的科学技术大军，要有一大批世界第一流的科学...		  【文件名:\当代\CWAC\AEB0001.txt	文章标题:	作者:】
#3 这一句话最后要求的结构是【1】序号+【2】出处+【3】清洗完成的句子+【4】所含有的aabb式,但是建表时要求再加【5】词性【6】依存句法关系
import re
from unittest import result
from pyltp import Segmentor#导入Segmentor库
from pyltp import Postagger#导入Postagger库
from pyltp import  Parser#导入库Parser
math_path = "D:\LTP\pyltp-0.2.1\pyltp.egg-info\ltp_data_v3.4.0\cws.model"#LTP分词模型库
math_path1 = "D:\LTP\pyltp-0.2.1\pyltp.egg-info\ltp_data_v3.4.0\pos.model"#LTP词性标注模型库
math_path2= "D:\LTP\pyltp-0.2.1\pyltp.egg-info\ltp_data_v3.4.0\parser.model"#LTP依存分析模型库
segmentor = Segmentor()#实例化分词模块
segmentor.load(math_path)#加载分词库
postagger = Postagger() #实例化词性模块
postagger.load(math_path1)#加载词性库
parser = Parser()  # 初始化实例 
parser.load(math_path2)#加载依存分析库
from numpy import source
import xlwt
#准备excel表
book = xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet = book.add_sheet('分析结果',cell_overwrite_ok=True)
col = ('序号','出处','清洗完成的句子','词性','依存句法关系','所含有的AABB式','句中对应部分')
for i in range(0,7):
		sheet.write(0,i,col[i])
ex_line=0
#863词性标注字典
_863dict = {
            'a': '形容词(adjective)', 
            'b': '其他名词修饰词(other noun-modifier)', 
            'c': '连词(conjunction)',
            'd': '副词(adverb)',
            'e': '叹词(exclamation)',
            'g': '语素(morpheme)',
            'h': '前缀(prefix)', 
            'i': '成语、习语(idiom)',
            'j': '缩写(abbreviation)',
            'k': '后缀(suffix)',
            'm': '数字(number)',
            'n': '一般名词(general noun)', 
            'nd': '方位名词(direction noun)',
            'nh': '人名(person name)',
            'ni': '机构名(organization name)',
            'nl': '位置名词(lacation name)',
            'ns': '地点名词(geographical name	)', 
            'nt': '时间名词(temporal noun)',
            'nz': '其他专有名词(other proper noun)',
            'o': '拟声词(onomatopoeia)',
            'p': '介词，前置词(preposition)',
            'q': '量词(quantity)',
            'r': '代词(pronoun)', 
            'u': '助词(auxiliary)',
            'v': '动词(verb)',
            'wp': '标点(punctuation)',
            'ws': '外文词(foreign words)',
            'x': '非词根(non-lexeme)', 
            'z': '状态词(descriptive words)'
            }
#句法关系字典(syntactic relationship dict)
_syn_rl_dict={
               'SBV':'主谓关系(subject-verb)',
               'VOB':'动宾关系(直接宾语，verb-object)',
               'IOB':'间宾关系(间接宾语，indirect-object)',
               'FOB':'前置宾语(前置宾语，fronting-object)',
               'DBL':'兼语(double)',
               'ATT':'定中关系(attribute)',
               'ADV':'状中结构(adverbial)',
               'CMP':'动补结构(complement)',
               'COO':'并列关系(coordinate)',
               'POB':'介宾关系(preposition-object)',
               'LAD':'左附加关系(left adjunct)',
               'RAD':'右附加关系(right adjunct)',
               'IS':'独立结构(independent structure)',
               'HED':'核心关系(head)',
               'WP':'符号卡位(人工二次清洗数据)'
             }
# 清洗句子的函数：逻辑是，从aabb所在的位置往两边扫描，一旦发现[。！“”；]则停止，好了之后返回处理好的句子
# [左边的情况，我们只需要找到符号最后一次出现的位置即可，rfind函数
# ]右边的情况，我们只需要找到符号最先出现的位置即可，find函数
def clean_sents(dir_sent):
  #从第一个字符找到第五个字符，截取冒号之前的数字的位置i,则序号为 dir_sent[0:i]
  i=dir_sent.rfind(':',1,6)
  #则有序号
  serial=dir_sent[0:i]
  #从左到右找到【为止的位置为j，则原文为 dir_sent[i+1:j]
  j=dir_sent.rfind("【")
  #则有出处
  source=dir_sent[j+1:dir_sent.rfind('】',j,)]
  #若字符串头部有“...”，则去掉
  if dir_sent[i+1:i+4]=='...':
    dir_sent=dir_sent[i+4:j]
  else:
    dir_sent=dir_sent[i+1:j]
  dir_sent=dir_sent.rstrip()
  #若字符串尾部有“...”，则去掉
  if dir_sent[-3:]=='...':
    dir_sent=dir_sent[:-3]
  #从左到右找到[为止的位置为k,则行句子中的AABB式为 dir_sent[k+1:k+5]
  k=dir_sent.rfind("[")
  #则有AABB,前包后不包
  aabb=dir_sent[k+1:k+5]
  #此时可以得到【1】序号【2】出处【3】不带...的原句，接下来继续清洗
  #左边的情况，如果找到符号的情况下，就把它们从左到右最后一个句子结束点后到AABB前一个字符的内容截取下来
  pos=[]
  if dir_sent.rfind('。',0,k)>0:pos.append(dir_sent.rfind('。',0,k))
  if dir_sent.rfind('！',0,k)>0:pos.append(dir_sent.rfind('！',0,k))
  if dir_sent.rfind('？',0,k)>0:pos.append(dir_sent.rfind('？',0,k))
  if dir_sent.rfind('；',0,k)>0:pos.append(dir_sent.rfind('；',0,k))
  if dir_sent.rfind('……',0,k)>0:pos.append(dir_sent.rfind('……',0,k)+1)
  if dir_sent.rfind('：“',0,k)>0:pos.append(dir_sent.rfind('：“',0,k)+1)
  if dir_sent.rfind('。”',0,k)>0:pos.append(dir_sent.rfind('。”',0,k)+1)
  if dir_sent.rfind('？”',0,k)>0:pos.append(dir_sent.rfind('？”',0,k)+1)
  if dir_sent.rfind('！”',0,k)>0:pos.append(dir_sent.rfind('！”',0,k)+1)
  if dir_sent.rfind('.”',0,k)>0:pos.append(dir_sent.rfind('.”',0,k)+1)
  if dir_sent.rfind('…”',0,k)>0:pos.append(dir_sent.rfind('…”',0,k)+1)
  if not pos:
    if dir_sent.rfind('，',0,k)>0:
      pos.append(dir_sent.rfind('，',0,k))
    else:
      pos.append(-1)
  pos.sort()
  pre=dir_sent[pos[-1]+1:k]
  #右边的情况，如果找到符号的情况下，就把它们从左到右第一个句子结束点截取下来
  pos.clear()
  if dir_sent.find('。',k+6)>0:pos.append(dir_sent.find('。',k+6))
  if dir_sent.find('！',k+6)>0:pos.append(dir_sent.find('！',k+6))
  if dir_sent.find('？',k+6)>0:pos.append(dir_sent.find('？',k+6))
  if dir_sent.find('；',k+6)>0:pos.append(dir_sent.find('；',k+6))
  if dir_sent.find('……',k+6)>0:pos.append(dir_sent.find('……',k+6))
  if dir_sent.find('。”',k+6)>0:pos.append(dir_sent.find('。”',k+6)+1)
  if dir_sent.find('？”',k+6)>0:pos.append(dir_sent.find('？”',k+6)+1)
  if dir_sent.find('！”',k+6)>0:pos.append(dir_sent.find('！”',k+6)+1)
  if dir_sent.find('.”',k+6)>0:pos.append(dir_sent.find('.”',k+6)+1)
  if dir_sent.find('…”',k+6)>0:pos.append(dir_sent.find('…”',k+6)+1)
  if not pos:pos.append(len(dir_sent))
  pos.sort()
  rear=dir_sent[k+6:pos[0]+1]
  pos.clear()
  #result则是清洗完成的句子
  #去除头尾空格
  result=(pre+aabb+rear).strip()
  #去除头部“
  result=result.lstrip('“')
  tuple=(serial,source,result,aabb)
  return tuple

with open("corpus_pattern_AABB.txt","r",errors='ignore')as f:#以只读方式打开文件
  for line in f.readlines():#对每一行进行循环操作
    line = line.strip('\n')#获取当前行
    #剔除非全是中文的AABB式
    k=line.rfind("[")
    aabb=line[k+1:k+5]
    if len(re.findall('([\u4e00-\u9fa5])',aabb))!=4:
      continue 
    tuple=clean_sents(line)
    serial=tuple[0]
    source=tuple[1]
    res=tuple[2]
    aabb=tuple[3]
    #用ltp进行词性标注
    #分词
    seg = segmentor.segment(res)
    #词性标注
    pos = postagger.postag(seg)
    #句法分析
    dep = parser.parse(seg, pos)  
    #找到aabb在划分后中的list的位置inc
    inc=-1
    for target in list(seg):
    #若能找到，则进行下一步分析
    #  if target.find(aabb)!=-1:
     if target==aabb:  
      inc=list(seg).index(target)
      break
    if inc!=-1:
      if len(re.findall('([\u4e00-\u9fa5])',seg[dep[inc].head-1]))!=0:
       #若解析出完整的AABB式且句法关系对应成分为汉字，则按列写入excel表
       ex_line+=1
       sheet.write(ex_line,0,serial)
       sheet.write(ex_line,1,source)
       sheet.write(ex_line,2,res)
       sheet.write(ex_line,3,_863dict[list(pos)[inc]])
       sheet.write(ex_line,4,_syn_rl_dict[dep[inc].relation])
       sheet.write(ex_line,5,aabb)
       sheet.write(ex_line,6,seg[dep[inc].head-1])   
savepath = 'C:/Users/senti/Desktop/excel表格.xls'
book.save(savepath)
segmentor.release()  # 释放模型
postagger.release()  # 释放模型
parser.release()  # 释放模型





  
  
  
     
     

