# JoyGamesHTTP
HTTP/HTTPS API Testing Tools for JoyGames QA

要注意protocol和http的区别
下周回来后理清一下

http/https的url区别，已经放在confighttp.py的get（）和post（）函数里完成了，通过字符串拼接和header
请求http还是https，由http_conf.ini控制，不需要额外传参数生成对象的时候控制

也就是说，任何代码里面！包括test_interface_case.py、 runcase.py 、main.py里面的传实餐，都是http，而不是protocol

protocol只是confighttp.py生成的http对象的一个属性，他的值http_conf.ini控制

恩，所以要注意：
1. 检查何代码里面！包括test_interface_case.py、 runcase.py 、main.py里面的传实餐，都是http，而不是protocol

2. 将http改成对象名，这个容易混淆，比如改成httpobject好多了！
