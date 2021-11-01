import asyncio
import threading

import websockets


class Server(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        while True:
            # 检测客户端权限，用户名密码通过才能退出循环
            async def check_permit(self, websocket):
                while True:
                    recv_str = await websocket.recv()
                    cred_dict = recv_str.split(":")
                    if cred_dict[0] == "admin" and cred_dict[1] == "123456":
                        response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
                        await websocket.send(response_str)
                        return True
                    else:
                        response_str = "sorry, the username or password is wrong, please submit again"
                        await websocket.send(response_str)

            # 服务器端主逻辑
            # websocket和path是该函数被回调时自动传过来的，不需要自己传
            # 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
            async def main_logic(websocket, path):
                while True:
                    recv_text = await websocket.recv()
                    response_text = f"your submit context: {recv_text}"
                    await websocket.send(response_text)

            async def main():
                async with websockets.serve(main_logic, "172.23.10.130", 1112):
                    await asyncio.Future()  # run forever

            asyncio.run(main())
            # 把ip换成自己本地的ip
            # start_server = websockets.serve(main_logic, "172.23.10.130", 1112)
            # 如果要给被回调的main_logic传递自定义参数，可使用以下形式
            # 一、修改回调形式
            # import functools
            # start_server = websockets.serve(functools.partial(main_logic, other_param="test_value"), '10.10.6.91', 5678)
            # 修改被回调函数定义，增加相应参数
            # async def main_logic(websocket, path, other_param)

            # asyncio.get_event_loop().run_until_complete(start_server)
            # asyncio.get_event_loop().run_forever()
