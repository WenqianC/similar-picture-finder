## similar-picture-finder

# 简介：
- python脚本图片查重器。用于个人收藏同人本的（购买/查重）管理。
- Mainly for doujinshi mass buyers, so you can check quickly whether you have bought one certain doujinshi.
- 适用于本子数量极多且无法记住封面的情况：比如你不会日语但买了几百本日文本子。
- 就是为了在收本的时候查一下之前买过没有。其他情况下没什么作用。
- 虽然速度很慢（主要是请求生成图片指纹的过程特别慢，不过这个只需要跑一次就行），但是效果还是很好的。比我找的其他人编的代码好。准确率很高。

# 原理：
- 借用了SAP推出的人工智能/机器学习平台，使用Leonardo提供的图片特征提取API。
- 代码整体框架基于：https://github.com/yejianquan/PictureSimilarityCompute/blob/master/README.md 感谢。（源码过时已更新。并基于自己的需求修改了。）

# 使用方法：
- 整理所有本子封面。我用的是【扫描全能王】，用【低画质扫描】一张张录入封面。它会自动切割无关区域，尽量不要使图中只出现封面。

- 首次使用
  - 自行安装：python(大版本是3.7就行），以及python的相关包：pip、request、numpy。
  - 注册https://api.sap.com/api/img_feature_extraction_api/resource ， 获取（show API key）你的API密钥。这是免费的。    

  - 下载这个文件夹
  - 用记事本打开文件夹下的两个.py文件，将你获得的密钥黏贴到【"APIKey":】后面（2个文件都要这么做）。假设密钥是1234，那么那一整行长这样：
    > "APIKey": "1234"

   
- 运行：
  - 若你有新的封面需要加入数据库：把图片放到needCalc文件夹下。在终端（或CMD）输入:
    > python picPreprocess.py
  - 若你已生成数据库，现在只需要检查checkBoughtOrNot文件夹里的本子有没有重复
  在终端（或CMD）输入:
    > python script.py

- 文件夹说明：
  - needCalc文件夹：用于暂存你拥有的本子的封面（也就是未处理的图）。运行程序picPreprocess.py时，程序会将已纳入数据库的图片移到dataPic文件夹下。
  - dataPic文件夹：用于存放已处理过的封面图。不要从这里移走，否则之后无法打开图片。
  - checkBoughtOrNot文件夹：这边放你想确认是否买过的本子的封面（也就是待购买清单）。获得结果后就可以删掉了。
  
- txt说明：
  - vectors.txt：是你的封面数据库。不要动它。
  - result.txt：是输出结果。其实没必要看它。因为计算完成后会自动打开图片的。
