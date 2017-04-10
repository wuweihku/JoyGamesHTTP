# JoyGamesHTTP
HTTP/HTTPS API Testing Tools for JoyGames QA

1. 支持request method扩展，get/post/put/delete等，甚至是socket.
2. 支持自定义测试接口场景的描述扩展，目前统一用test_interface_case通用接口测试函数，对于比较复杂的测试流程，可以额外定义函数,支持拓展.
3. 支持http/https 双协议头选择，及自定义headers描述.
4. 支持cookie
5. 支持通过在HTTP response 的header 中设置cookie 实现session 机制。


要注意protocol和http的区别
下周回来后理清一下

http/https的url区别，已经放在confighttp.py的get（）和post（）函数里完成了，通过字符串拼接和header
请求http还是https，由http_conf.ini控制，不需要额外传参数生成对象的时候控制

也就是说，任何代码里面！包括test_interface_case.py、 runcase.py 、main.py里面的传实餐，都是http，而不是protocol

protocol只是confighttp.py生成的http对象的一个属性，他的值http_conf.ini控制

恩，所以要注意：
1. 检查何代码里面！包括test_interface_case.py、 runcase.py 、main.py里面的传实餐，都是http，而不是protocol

2. 将http改成对象名，这个容易混淆，比如改成httpobject好多了！
