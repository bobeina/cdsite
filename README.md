cdsite
======

webgame,cthulhu dice,django,mysql,python

这是一个根桌游“克苏鲁之骰”改编而来的web游戏。使用的python版本：2.7.3 django版本：1.6.2
未测试在windows下运行情况。

假如有人想要自己下载这个游戏并安装，你需要在运行前修改以下行：
cthulhudice/view.py Line 20: 把cthulhudice/module的位置改成实际所在目录；
cdsite/settings.py Line 66-68：此处为mysql的连接设置，请将其修改为你自己的数据库名、用户名及密码；
cthulhudice/templates/chat/chat.html Line 180: 修改该网址为你自己的主机网址。

------------------------------------------------------
This is a webgame bases the table game "cthulhu dice". Python: v2.7.3 Django:v1.6.2

You need to modify these lines before you run it in your own host:
cthulhudice/view.py Line 20: modify directory of cthulhudice/module to actual one;
cdsite/settings.py Line 66-68：change to your dbname/username/passwd;
cthulhudice/templates/chat/chat.html Line 180: change to your actual web url.
