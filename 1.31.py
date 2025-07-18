import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import sys
import webbrowser
import socket
import threading
import time
import json

class NetworkRockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("智能石头剪刀布 - 局域网联机版")
        self.root.geometry("500x450")
        
        # 开源地址
        self.github_url = "https://github.com/cheyunze666/-"
        
        # 网络设置
        self.server_socket = None
        self.client_socket = None
        self.is_host = False
        self.is_client = False
        self.connection_status = "未连接"
        self.opponent_name = "对手"
        self.player_name = "玩家"
        self.port = 12345
        
        # 游戏设置
        self.win_target = 3
        self.player_choices = []
        self.ai_prediction_weight = 0.6
        
        # 分数
        self.player_score = 0
        self.opponent_score = 0
        
        # 初始化界面
        self.create_menu()
        self.create_network_frame()
        self.create_game_frame()
        self.add_about_info()
        
        # 设置玩家名字
        self.set_player_name()
        
        # 隐藏控制台窗口
        self.hide_console()

    def hide_console(self):
        """隐藏控制台窗口（仅适用于Windows）"""
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.WinDLL('kernel32')
                user32 = ctypes.WinDLL('user32')
                hwnd = kernel32.GetConsoleWindow()
                if hwnd:
                    user32.ShowWindow(hwnd, 0)
            except:
                pass

    def set_player_name(self):
        """设置玩家名称"""
        name = simpledialog.askstring("玩家名称", "请输入你的名字:", 
                                     parent=self.root,
                                     initialvalue="玩家")
        if name and name.strip():
            self.player_name = name.strip()
            self.player_name_label.config(text=f"玩家: {self.player_name}")
        else:
            self.player_name = "玩家"
            self.player_name_label.config(text="玩家: 玩家")

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 游戏菜单
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="游戏", menu=game_menu)
        game_menu.add_command(label="设置获胜条件", command=self.set_win_target)
        game_menu.add_command(label="重新开始", command=self.reset_game)
        game_menu.add_separator()
        game_menu.add_command(label="退出", command=self.root.quit)
        
        # 网络菜单
        network_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="网络", menu=network_menu)
        network_menu.add_command(label="创建主机", command=self.create_host)
        network_menu.add_command(label="加入游戏", command=self.join_game)
        network_menu.add_command(label="断开连接", command=self.disconnect)
        network_menu.add_command(label="设置玩家名称", command=self.set_player_name)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="游戏规则", command=self.show_rules)
        help_menu.add_command(label="关于", command=self.show_about)
        help_menu.add_command(label="访问开源地址", command=self.open_github)

    def create_network_frame(self):
        """创建网络连接状态面板"""
        network_frame = tk.LabelFrame(self.root, text="网络连接", padx=10, pady=5)
        network_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 连接状态
        status_frame = tk.Frame(network_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(status_frame, text="状态:").pack(side=tk.LEFT)
        self.status_label = tk.Label(status_frame, text=self.connection_status, fg="red")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # 玩家信息
        player_frame = tk.Frame(network_frame)
        player_frame.pack(fill=tk.X, pady=5)
        
        self.player_name_label = tk.Label(player_frame, text="玩家: 未设置")
        self.player_name_label.pack(side=tk.LEFT, padx=5)
        
        tk.Label(player_frame, text="|").pack(side=tk.LEFT, padx=5)
        
        self.opponent_label = tk.Label(player_frame, text=f"{self.opponent_name}: 未连接")
        self.opponent_label.pack(side=tk.LEFT, padx=5)
        
        # 网络操作按钮
        btn_frame = tk.Frame(network_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.host_btn = tk.Button(btn_frame, text="创建主机", width=10, command=self.create_host)
        self.host_btn.pack(side=tk.LEFT, padx=5)
        
        self.join_btn = tk.Button(btn_frame, text="加入游戏", width=10, command=self.join_game)
        self.join_btn.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_btn = tk.Button(btn_frame, text="断开连接", width=10, 
                                      command=self.disconnect, state=tk.DISABLED)
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)

    def create_game_frame(self):
        """创建游戏面板"""
        game_frame = tk.LabelFrame(self.root, text="游戏", padx=10, pady=5)
        game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 分数显示
        score_frame = tk.Frame(game_frame)
        score_frame.pack(fill=tk.X, pady=5)
        
        self.target_label = tk.Label(score_frame, text=f"获胜条件: 先赢得 {self.win_target} 局")
        self.target_label.pack()
        
        self.score_label = tk.Label(score_frame, text=f"{self.player_name}: 0  |  {self.opponent_name}: 0", 
                                   font=("Arial", 14))
        self.score_label.pack(pady=5)
        
        # 状态显示
        self.status_label = tk.Label(game_frame, text="请选择你的出拳", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # 游戏按钮
        button_frame = tk.Frame(game_frame)
        button_frame.pack(pady=10)
        
        self.rock_btn = tk.Button(button_frame, text="石头 (1)", width=10, height=2,
                                 command=lambda: self.play_game(1), state=tk.DISABLED)
        self.rock_btn.pack(side=tk.LEFT, padx=10)
        
        self.scissors_btn = tk.Button(button_frame, text="剪刀 (2)", width=10, height=2,
                                    command=lambda: self.play_game(2), state=tk.DISABLED)
        self.scissors_btn.pack(side=tk.LEFT, padx=10)
        
        self.paper_btn = tk.Button(button_frame, text="布 (3)", width=10, height=2,
                                 command=lambda: self.play_game(3), state=tk.DISABLED)
        self.paper_btn.pack(side=tk.LEFT, padx=10)
        
        # 规则提示
        rule_tip = tk.Label(game_frame, text="游戏规则提示: 石头(1) > 剪刀(2) > 布(3) > 石头(1)", 
                           font=("Arial", 9), fg="green")
        rule_tip.pack(pady=5)
        
        # 结果标签
        self.result_label = tk.Label(game_frame, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)
        
        # 等待提示
        self.waiting_label = tk.Label(game_frame, text="", font=("Arial", 10), fg="blue")
        self.waiting_label.pack(pady=5)

    def add_about_info(self):
        """添加关于信息"""
        about_frame = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        about_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        # 开发者信息
        dev_label = tk.Label(about_frame, text="此游戏为烂香蕉一人开发", font=("Arial", 8), fg="gray")
        dev_label.pack(pady=2)
        
        # 开源链接
        github_frame = tk.Frame(about_frame)
        github_frame.pack(pady=2)
        
        github_label = tk.Label(github_frame, text="开源地址: ", font=("Arial", 8), fg="gray")
        github_label.pack(side=tk.LEFT)
        
        self.github_link = tk.Label(github_frame, text=self.github_url, 
                                  font=("Arial", 8, "underline"), fg="blue", cursor="hand2")
        self.github_link.pack(side=tk.LEFT)
        self.github_link.bind("<Button-1>", lambda e: self.open_github())
        
        tip_label = tk.Label(about_frame, text="点击链接访问项目源码", font=("Arial", 7), fg="gray")
        tip_label.pack(pady=1)

    def open_github(self):
        """打开GitHub开源地址"""
        try:
            webbrowser.open(self.github_url)
        except:
            messagebox.showerror("错误", f"无法打开链接\n请手动访问: {self.github_url}")

    def show_rules(self):
        """显示游戏规则"""
        rules_text = (
            "📜 石头剪刀布游戏规则 📜\n\n"
            "1. 基本规则：\n"
            "   - 石头(1) 打败 剪刀(2)\n"
            "   - 剪刀(2) 打败 布(3)\n"
            "   - 布(3) 打败 石头(1)\n"
            "   - 相同则为平局\n\n"
            
            "2. 联机模式：\n"
            "   - 一个玩家创建主机，另一个加入游戏\n"
            "   - 双方轮流出拳，系统自动判断胜负\n"
            "   - 先赢得设定局数的一方获胜\n\n"
            
            "3. 获胜条件：\n"
            "   - 先赢得设定局数的一方获胜（默认3局）\n"
            "   - 可在【游戏】菜单中修改获胜条件\n\n"
            
            "4. 网络设置：\n"
            "   - 确保双方在同一局域网\n"
            "   - 主机无需额外设置\n"
            "   - 客户端需要输入主机的IP地址\n\n"
            
            "5. 开源信息：\n"
            f"   - 项目地址: {self.github_url}\n\n"
            
            "🎮 祝你游戏愉快！🎮"
        )
        messagebox.showinfo("游戏规则", rules_text)

    def show_about(self):
        """显示关于信息"""
        about_text = (
            "石头剪刀布游戏 - 局域网联机版\n\n"
            "版本: 2.0\n"
            "开发人员: 烂香蕉\n\n"
            "此游戏为烂香蕉一人开发\n"
            "版权所有 © 2023\n\n"
            f"开源地址: {self.github_url}\n"
            "点击'访问开源地址'可查看项目源码"
        )
        messagebox.showinfo("关于", about_text)

    def set_win_target(self):
        """设置获胜条件"""
        try:
            new_target = simpledialog.askinteger("设置获胜条件", 
                                               f"请输入新的获胜局数 (当前: {self.win_target}):",
                                               parent=self.root,
                                               minvalue=1, maxvalue=10)
            if new_target:
                self.win_target = new_target
                self.target_label.config(text=f"获胜条件: 先赢得 {self.win_target} 局")
                self.check_game_end()
        except:
            messagebox.showerror("错误", "请输入有效的数字")

    def get_local_ip(self):
        """获取本机IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "无法获取IP"

    def create_host(self):
        """创建游戏主机"""
        if self.is_host or self.is_client:
            messagebox.showwarning("警告", "请先断开当前连接")
            return
            
        self.is_host = True
        self.connection_status = "等待玩家连接..."
        self.update_network_status()
        
        # 创建服务器线程
        threading.Thread(target=self.run_server, daemon=True).start()
        
        # 显示主机IP
        ip = self.get_local_ip()
        messagebox.showinfo("主机已创建", 
                          f"主机已创建，等待玩家连接...\n"
                          f"你的IP地址: {ip}\n"
                          f"端口: {self.port}\n\n"
                          "请将此信息告诉其他玩家")

    def run_server(self):
        """运行服务器"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(1)
            
            self.root.after(0, lambda: self.waiting_label.config(text="等待玩家连接..."))
            
            self.client_socket, addr = self.server_socket.accept()
            self.is_client = True  # 主机同时也作为客户端连接
            
            self.connection_status = f"已连接: {addr[0]}"
            self.opponent_name = "玩家2"
            self.root.after(0, self.update_network_status)
            self.root.after(0, lambda: self.waiting_label.config(text=""))
            self.root.after(0, self.enable_game_buttons)
            
            # 发送玩家名称
            self.send_data({
                'type': 'player_info',
                'name': self.player_name
            })
            
            # 开始接收数据
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"创建主机失败: {str(e)}"))
            self.disconnect()

    def join_game(self):
        """加入游戏"""
        if self.is_host or self.is_client:
            messagebox.showwarning("警告", "请先断开当前连接")
            return
            
        ip = simpledialog.askstring("加入游戏", "请输入主机IP地址:", parent=self.root)
        if not ip:
            return
            
        self.is_client = True
        self.connection_status = f"连接中: {ip}..."
        self.update_network_status()
        
        # 创建客户端线程
        threading.Thread(target=self.connect_to_host, args=(ip,), daemon=True).start()

    def connect_to_host(self, ip):
        """连接到主机"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, self.port))
            
            self.connection_status = f"已连接: {ip}"
            self.opponent_name = "玩家1"
            self.root.after(0, self.update_network_status)
            self.root.after(0, self.enable_game_buttons)
            
            # 发送玩家名称
            self.send_data({
                'type': 'player_info',
                'name': self.player_name
            })
            
            # 开始接收数据
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"连接失败: {str(e)}"))
            self.disconnect()

    def disconnect(self):
        """断开连接"""
        self.connection_status = "未连接"
        self.opponent_name = "对手"
        self.update_network_status()
        
        self.is_host = False
        self.is_client = False
        
        # 关闭套接字
        try:
            if self.server_socket:
                self.server_socket.close()
            if self.client_socket:
                self.client_socket.close()
        except:
            pass
            
        self.server_socket = None
        self.client_socket = None
        
        # 禁用游戏按钮
        self.rock_btn.config(state=tk.DISABLED)
        self.scissors_btn.config(state=tk.DISABLED)
        self.paper_btn.config(state=tk.DISABLED)
        
        self.waiting_label.config(text="")
        self.result_label.config(text="")
        self.status_label.config(text="请选择你的出拳")

    def update_network_status(self):
        """更新网络状态显示"""
        self.status_label.config(text=self.connection_status)
        self.opponent_label.config(text=f"{self.opponent_name}: {'已连接' if self.is_client else '未连接'}")
        
        # 更新按钮状态
        if self.is_host or self.is_client:
            self.host_btn.config(state=tk.DISABLED)
            self.join_btn.config(state=tk.DISABLED)
            self.disconnect_btn.config(state=tk.NORMAL)
        else:
            self.host_btn.config(state=tk.NORMAL)
            self.join_btn.config(state=tk.NORMAL)
            self.disconnect_btn.config(state=tk.DISABLED)
        
        # 更新分数显示
        self.score_label.config(text=f"{self.player_name}: {self.player_score}  |  {self.opponent_name}: {self.opponent_score}")

    def enable_game_buttons(self):
        """启用游戏按钮"""
        self.rock_btn.config(state=tk.NORMAL)
        self.scissors_btn.config(state=tk.NORMAL)
        self.paper_btn.config(state=tk.NORMAL)
        self.status_label.config(text="请选择你的出拳")

    def send_data(self, data):
        """发送数据"""
        if not self.client_socket:
            return
            
        try:
            json_data = json.dumps(data).encode('utf-8')
            self.client_socket.sendall(json_data)
        except:
            self.root.after(0, lambda: messagebox.showerror("错误", "发送数据失败，连接可能已断开"))
            self.disconnect()

    def receive_data(self):
        """接收数据"""
        while self.client_socket:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                    
                json_data = json.loads(data.decode('utf-8'))
                self.handle_received_data(json_data)
            except:
                self.root.after(0, lambda: messagebox.showerror("错误", "连接已断开"))
                self.disconnect()
                break

    def handle_received_data(self, data):
        """处理接收到的数据"""
        if data['type'] == 'player_info':
            self.opponent_name = data['name']
            self.root.after(0, self.update_network_status)
        elif data['type'] == 'choice':
            opponent_choice = data['choice']
            self.root.after(0, lambda: self.process_round(opponent_choice))
        elif data['type'] == 'result':
            self.player_score = data['player_score']
            self.opponent_score = data['opponent_score']
            self.root.after(0, self.update_network_status)
            self.root.after(0, self.check_game_end)

    def play_game(self, player_choice):
        """玩家出拳"""
        if not self.is_client:
            messagebox.showwarning("警告", "请先连接到游戏")
            return
            
        # 发送选择给对手
        self.send_data({
            'type': 'choice',
            'choice': player_choice
        })
        
        # 显示选择
        choices = {1: "石头(1)", 2: "剪刀(2)", 3: "布(3)"}
        player_name = choices[player_choice]
        self.status_label.config(text=f"你选择了: {player_name}")
        self.result_label.config(text="等待对手出拳...")
        
        # 禁用按钮等待对手
        self.rock_btn.config(state=tk.DISABLED)
        self.scissors_btn.config(state=tk.DISABLED)
        self.paper_btn.config(state=tk.DISABLED)
        self.waiting_label.config(text="等待对手出拳...")

    def process_round(self, opponent_choice):
        """处理一局游戏"""
        # 获取玩家选择（从最后的选择中获取）
        if not self.player_choices:
            return
            
        player_choice = self.player_choices[-1]
        
        # 获取选择名称
        choices = {1: "石头(1)", 2: "剪刀(2)", 3: "布(3)"}
        player_name = choices[player_choice]
        opponent_name = choices[opponent_choice]
        
        # 显示选择
        self.status_label.config(text=f"你选择了: {player_name}, {self.opponent_name}选择了: {opponent_name}")
        
        # 判断胜负
        result = self.determine_winner(player_choice, opponent_choice)
        self.result_label.config(text=f"结果: {result}")
        
        # 更新分数
        if "赢" in result:
            self.player_score += 1
        elif "输" in result:
            self.opponent_score += 1
        
        self.update_network_status()
        
        # 发送结果给对手
        self.send_data({
            'type': 'result',
            'player_score': self.player_score,
            'opponent_score': self.opponent_score
        })
        
        # 检查游戏是否结束
        self.check_game_end()
        
        # 启用按钮准备下一轮
        self.enable_game_buttons()
        self.waiting_label.config(text="")

    def determine_winner(self, player, opponent):
        if player == opponent:
            return "平局！"
        
        # 石头(1)赢剪刀(2), 剪刀(2)赢布(3), 布(3)赢石头(1)
        if (player == 1 and opponent == 2) or \
           (player == 2 and opponent == 3) or \
           (player == 3 and opponent == 1):
            return "你赢了！"
        
        return "你输了！"

    def check_game_end(self):
        """检查游戏是否结束"""
        if self.player_score >= self.win_target or self.opponent_score >= self.win_target:
            # 禁用游戏按钮
            self.rock_btn.config(state=tk.DISABLED)
            self.scissors_btn.config(state=tk.DISABLED)
            self.paper_btn.config(state=tk.DISABLED)
            
            # 显示获胜信息
            if self.player_score >= self.win_target:
                winner = self.player_name
                message = f"恭喜！{self.player_name}获胜！"
            else:
                winner = self.opponent_name
                message = f"{self.opponent_name}获胜！"
                
            messagebox.showinfo("游戏结束", 
                               f"{message}\n"
                               f"最终比分: {self.player_name} {self.player_score} - {self.opponent_name} {self.opponent_score}")
            
            # 提供重新开始选项
            self.restart_prompt()

    def restart_prompt(self):
        """游戏结束后提示重新开始"""
        response = messagebox.askyesno("游戏结束", "是否要重新开始游戏？")
        if response:
            self.reset_game()

    def reset_game(self):
        """重置游戏"""
        self.player_score = 0
        self.opponent_score = 0
        self.player_choices = []
        
        self.update_network_status()
        self.result_label.config(text="")
        self.status_label.config(text="请选择你的出拳")
        
        if self.is_client:
            self.enable_game_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    game = NetworkRockPaperScissors(root)
    root.mainloop()
