import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import sys

class SmartRockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("智能石头剪刀布")
        self.root.geometry("450x380")
        
        # 隐藏控制台窗口
        self.hide_console()
        
        # 初始化游戏设置
        self.win_target = 3
        self.player_choices = []  # 存储玩家历史选择
        self.ai_prediction_weight = 0.6  # AI预测权重（0.0-1.0）
        
        # 初始化分数
        self.player_score = 0
        self.ai_score = 0
        
        # 创建菜单
        self.create_menu()
        
        # 创建界面元素
        self.create_widgets()
        self.update_score_display()
        
        # 添加关于信息
        self.add_about_info()

    def hide_console(self):
        """隐藏控制台窗口（仅适用于Windows）"""
        if sys.platform == 'win32':
            try:
                # 尝试隐藏控制台窗口
                import ctypes
                kernel32 = ctypes.WinDLL('kernel32')
                user32 = ctypes.WinDLL('user32')
                hwnd = kernel32.GetConsoleWindow()
                if hwnd:
                    user32.ShowWindow(hwnd, 0)  # 0 = SW_HIDE
            except:
                # 如果失败，建议用户保存为.pyw文件
                messagebox.showinfo("提示", 
                    "为了完全隐藏控制台窗口，请将文件保存为.pyw扩展名")

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
        
        # AI设置菜单
        ai_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="AI设置", menu=ai_menu)
        ai_menu.add_command(label="设置AI智能级别", command=self.set_ai_level)
        ai_menu.add_command(label="重置AI记忆", command=self.reset_ai_memory)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="游戏规则", command=self.show_rules)  # 新增游戏规则选项
        help_menu.add_command(label="关于", command=self.show_about)

    def show_rules(self):
        """显示游戏规则对话框"""
        rules_text = (
            "📜 石头剪刀布游戏规则 📜\n\n"
            "1. 基本规则：\n"
            "   - 石头(1) 打败 剪刀(2)\n"
            "   - 剪刀(2) 打败 布(3)\n"
            "   - 布(3) 打败 石头(1)\n"
            "   - 相同则为平局\n\n"
            
            "2. 游戏玩法：\n"
            "   - 点击【石头】【剪刀】【布】按钮选择你的出拳\n"
            "   - AI会智能预测并出拳\n"
            "   - 每轮结果会显示在界面上\n\n"
            
            "3. 获胜条件：\n"
            "   - 先赢得设定局数的一方获胜（默认3局）\n"
            "   - 可在【游戏】菜单中修改获胜条件\n\n"
            
            "4. AI智能系统：\n"
            "   - AI会学习你的出拳模式并尝试预测\n"
            "   - 可在【AI设置】菜单调整智能级别\n"
            "   - 可随时重置AI记忆\n\n"
            
            "5. 其他功能：\n"
            "   - 界面底部显示历史出拳统计数据\n"
            "   - 实时显示AI预测结果\n"
            "   - 游戏结束时可重新开始\n\n"
            
            "🎮 祝你游戏愉快！🎮"
        )
        messagebox.showinfo("游戏规则", rules_text)

    def show_about(self):
        """显示关于对话框"""
        about_text = (
            "石头剪刀布游戏\n\n"
            "版本: 1.2\n"
            "开发人员: 烂香蕉\n\n"
            "此游戏为烂香蕉一人开发\n"
            "版权所有 © 2023\n"
        )
        messagebox.showinfo("关于", about_text)

    def add_about_info(self):
        """在界面底部添加关于信息"""
        about_frame = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        about_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        about_label = tk.Label(
            about_frame, 
            text="此游戏为烂香蕉一人开发", 
            font=("Arial", 8),
            fg="gray"
        )
        about_label.pack(pady=2)

    def create_widgets(self):
        # 标题标签
        self.title_label = tk.Label(self.root, text="智能石头剪刀布游戏", 
                                   font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        # 获胜条件显示
        self.target_label = tk.Label(self.root, text=f"获胜条件: 先赢得 {self.win_target} 局", 
                                   font=("Arial", 10))
        self.target_label.pack()
        
        # 分数显示
        self.score_label = tk.Label(self.root, text="玩家: 0  |  AI: 0", 
                                   font=("Arial", 14))
        self.score_label.pack(pady=5)
        
        # 状态显示
        self.status_label = tk.Label(self.root, text="请选择你的出拳", 
                                   font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # 游戏按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # 游戏按钮
        self.rock_btn = tk.Button(button_frame, text="石头 (1)", width=10, height=2,
                                 command=lambda: self.play_game(1))
        self.rock_btn.pack(side=tk.LEFT, padx=10)
        
        self.scissors_btn = tk.Button(button_frame, text="剪刀 (2)", width=10, height=2,
                                    command=lambda: self.play_game(2))
        self.scissors_btn.pack(side=tk.LEFT, padx=10)
        
        self.paper_btn = tk.Button(button_frame, text="布 (3)", width=10, height=2,
                                 command=lambda: self.play_game(3))
        self.paper_btn.pack(side=tk.LEFT, padx=10)
        
        # 规则提示标签
        rule_tip = tk.Label(self.root, text="游戏规则提示: 石头(1) > 剪刀(2) > 布(3) > 石头(1)", 
                           font=("Arial", 9), fg="green")
        rule_tip.pack(pady=5)
        
        # 结果标签
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)
        
        # AI预测标签
        self.ai_prediction_label = tk.Label(self.root, text="AI预测: 无", 
                                          font=("Arial", 10), fg="blue")
        self.ai_prediction_label.pack(pady=5)
        
        # 历史记录标签
        self.history_label = tk.Label(self.root, text="历史: 无", 
                                    font=("Arial", 9), fg="gray")
        self.history_label.pack(pady=5)

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
                self.check_game_end()  # 检查是否已经达到新的获胜条件
        except:
            messagebox.showerror("错误", "请输入有效的数字")

    def set_ai_level(self):
        """设置AI智能级别"""
        try:
            level = simpledialog.askfloat("设置AI智能级别", 
                                         "AI预测权重 (0.0-1.0):\n"
                                         "0.0 = 完全随机\n"
                                         "0.5 = 中等智能\n"
                                         "1.0 = 最大预测\n"
                                         f"当前: {self.ai_prediction_weight}",
                                         parent=self.root,
                                         minvalue=0.0, maxvalue=1.0)
            if level is not None:
                self.ai_prediction_weight = round(level, 1)
                messagebox.showinfo("AI设置", f"AI预测权重已设置为: {self.ai_prediction_weight}")
        except:
            messagebox.showerror("错误", "请输入0.0到1.0之间的数字")

    def reset_ai_memory(self):
        """重置AI记忆"""
        self.player_choices = []
        self.ai_prediction_label.config(text="AI预测: 无")
        self.history_label.config(text="历史: 无")
        messagebox.showinfo("AI重置", "AI记忆已清除，将重新开始学习")

    def smart_ai_choice(self):
        """智能AI选择 - 基于玩家历史出拳模式"""
        # 如果没有历史记录，随机选择
        if not self.player_choices or random.random() > self.ai_prediction_weight:
            return random.randint(1, 3)
        
        # 分析玩家历史选择模式
        last_choice = self.player_choices[-1]
        
        # 进阶策略：分析历史模式
        # 计算玩家选择每种选项的概率
        count_rock = self.player_choices.count(1)
        count_scissors = self.player_choices.count(2)
        count_paper = self.player_choices.count(3)
        total = len(self.player_choices)
        
        # 计算概率
        prob_rock = count_rock / total
        prob_scissors = count_scissors / total
        prob_paper = count_paper / total
        
        # 预测玩家最可能的选择
        predicted_player_choice = max([(prob_rock, 1), (prob_scissors, 2), (prob_paper, 3)])[1]
        
        # 显示预测
        choices_name = {1: "石头(1)", 2: "剪刀(2)", 3: "布(3)"}
        self.ai_prediction_label.config(text=f"AI预测: 玩家可能出 {choices_name[predicted_player_choice]}")
        
        # 更新历史显示
        history_text = f"历史: 石头({count_rock}/{total}) 剪刀({count_scissors}/{total}) 布({count_paper}/{total})"
        self.history_label.config(text=history_text)
        
        # 选择能击败预测的选项
        if predicted_player_choice == 1:  # 石头
            return 3  # 布
        elif predicted_player_choice == 2:  # 剪刀
            return 1  # 石头
        else:  # 布
            return 2  # 剪刀

    def play_game(self, player_choice):
        """进行一局游戏"""
        # 记录玩家选择
        self.player_choices.append(player_choice)
        
        # AI智能选择
        ai_choice = self.smart_ai_choice()
        
        # 获取选择名称
        choices = {1: "石头(1)", 2: "剪刀(2)", 3: "布(3)"}
        player_name = choices[player_choice]
        ai_name = choices[ai_choice]
        
        # 显示选择
        self.status_label.config(text=f"你选择了: {player_name}, AI选择了: {ai_name}")
        
        # 判断胜负
        result = self.determine_winner(player_choice, ai_choice)
        self.result_label.config(text=f"结果: {result}")
        
        # 更新分数
        if "赢" in result:
            self.player_score += 1
        elif "输" in result:
            self.ai_score += 1
        
        self.update_score_display()
        
        # 检查游戏是否结束
        self.check_game_end()

    def determine_winner(self, player, ai):
        if player == ai:
            return "平局！"
        
        # 石头(1)赢剪刀(2), 剪刀(2)赢布(3), 布(3)赢石头(1)
        if (player == 1 and ai == 2) or \
           (player == 2 and ai == 3) or \
           (player == 3 and ai == 1):
            return "你赢了！"
        
        return "你输了！"

    def update_score_display(self):
        self.score_label.config(text=f"玩家: {self.player_score}  |  AI: {self.ai_score}")

    def check_game_end(self):
        """检查游戏是否结束"""
        if self.player_score >= self.win_target or self.ai_score >= self.win_target:
            # 禁用游戏按钮
            self.rock_btn.config(state=tk.DISABLED)
            self.scissors_btn.config(state=tk.DISABLED)
            self.paper_btn.config(state=tk.DISABLED)
            
            # 显示获胜信息
            winner = "玩家" if self.player_score >= self.win_target else "AI"
            messagebox.showinfo("游戏结束", f"{winner}获胜！\n最终比分: {self.player_score}-{self.ai_score}")
            
            # 提供重新开始选项
            self.restart_prompt()

    def restart_prompt(self):
        """游戏结束后的重新开始提示"""
        response = messagebox.askyesno("游戏结束", "是否要重新开始游戏？")
        if response:
            self.reset_game()

    def reset_game(self):
        """重置游戏"""
        # 重置分数
        self.player_score = 0
        self.ai_score = 0
        
        # 重置显示
        self.update_score_display()
        self.status_label.config(text="请选择你的出拳")
        self.result_label.config(text="")
        self.ai_prediction_label.config(text="AI预测: 无")
        self.history_label.config(text="历史: 无")
        
        # 启用游戏按钮
        self.rock_btn.config(state=tk.NORMAL)
        self.scissors_btn.config(state=tk.NORMAL)
        self.paper_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = SmartRockPaperScissors(root)
    root.mainloop()