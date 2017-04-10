# JoyGamesHTTP
HTTP/HTTPS API Testing Tools for JoyGames QA

1. 支持request method扩展，get/post/put/delete等，甚至是socket.
2. 支持自定义测试接口场景的描述扩展，目前统一用test_interface_case通用接口测试函数，对于比较复杂的测试流程，可以额外定义函数,支持拓展.
3. 支持http/https 双协议头选择，及自定义headers描述.
4. 支持cookie
5. 支持通过在HTTP response 的header 中设置cookie 实现session 机制。



明天处理：
1. 配置文件的集中处理，不要太分散
