import pygame
# 导入game_items模块中的所有功能
from game_items import *


class Game(object):
    def __init__(self):
        # 创建游戏主窗口 set_mode方法
        self.main_window = pygame.display.set_mode((640, 480))
        # 设置窗口标题 set_caption方法
        pygame.display.set_caption('贪吃蛇')
        self.score_label = Label()  # 得分的标签
        self.tip_label = Label(24, False)  # 暂停或游戏结束的提示的标签
        self.is_game_over = False  # 游戏是否结束的标记，如果是True则说明游戏已经结束
        self.is_pause = False  # 游戏是否暂停的标记，如果是True则说明游戏已经被暂停
        self.food = Food()  # 食物
        self.snake = Snake()  # 贪吃蛇

    def start(self):
        """启动并控制游戏"""
        # 游戏时钟 time模块的Clock类用于刷新频率
        clock = pygame.time.Clock()
        # 保持窗口显示 死循环
        while True:
            # 事件监听 遍历同一时刻发生的事件列表
            for event in pygame.event.get():
                # 判断退出事件
                if event.type == pygame.QUIT:
                    return  # 点叉直接退出
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # 按ESC键退出
                    elif event.key == pygame.K_SPACE:
                        if self.is_game_over:
                            self.reset_game()
                        else:
                            self.is_pause = not self.is_pause  # 切换暂停状态
                if not self.is_pause and not self.is_game_over:
                    # 只有当游戏没暂停也没结束才需要更新食物位置
                    if event.type == FOOD_UPDATE_EVENT:
                        # 更新食物位置
                        self.food.random_rect()
                    elif event.type == SNAKE_UPDATE_EVENT:
                        # 移动蛇的位置 死了就game over
                        self.is_game_over = not self.snake.update()
                    elif event.type == pygame.KEYDOWN:
                        # 有按键按下 只要是上下左右中的一个就更改方向
                        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                            self.snake.change_dir(event.key)
            # 设置窗口背景颜色 fill填充颜色 RGB的元组
            self.main_window.fill(BACKGROUND_COLOR)
            # 绘制得分
            self.score_label.draw(self.main_window, "得分：%d" % self.snake.score)
            # 绘制提示暂停或者游戏结束的标签
            if self.is_pause:
                self.tip_label.draw(self.main_window, "游戏暂停，按空格键继续...")
            elif self.is_game_over:
                self.tip_label.draw(self.main_window, "游戏结束，按空格键开启新游戏")
            elif self.snake.has_eat(self.food):
                self.food.random_rect()
            # 绘制食物
            self.food.draw(self.main_window)
            # 绘制贪吃蛇
            self.snake.draw(self.main_window)
            # 刷新窗口内容 update
            pygame.display.update()
            # 设置刷新频率 tick 1秒钟刷新60帧
            clock.tick(60)

    def reset_game(self):
        """重置游戏参数"""
        self.score = 0
        self.is_game_over = False
        self.is_pause = False
        # 重置蛇的数据
        self.snake.reset_snake()
        # 重置食物的位置
        self.food.random_rect()


if __name__ == '__main__':
    # 游戏开始时要初始化 pygame 的模块
    pygame.init()
    # 游戏逻辑
    Game().start()
    # 游戏结束时要释放 pygame 模块占用的资源
    pygame.quit()
