import pygame
from src.generator import is_valid

# 颜色常量
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)      # 原始题目数字
RED = (255, 0, 0)        # 正在填入的数字
GREEN = (0, 180, 0)      # 已确认的数字
GRAY = (200, 200, 200)

class SudokuVisualizer:
    def __init__(self, puzzle, solution):
        pygame.init()
        self.screen = pygame.display.set_mode((540, 600))
        pygame.display.set_caption("数独求解过程可视化")
        self.font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 24)
        self.puzzle = puzzle.copy()
        self.solution = solution
        self.current_grid = puzzle.copy()
        self.steps = []          # 存储每一步：(row, col, num, status)
        self.current_step = 0
        self.running = True
        self.clock = pygame.time.Clock()
    
    def draw_grid(self):
        """绘制 9x9 网格"""
        self.screen.fill(WHITE)
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK, 
                             (50 + i*50, 50), (50 + i*50, 500), line_width)
            pygame.draw.line(self.screen, BLACK,
                             (50, 50 + i*50), (500, 50 + i*50), line_width)
    
    def draw_numbers(self, highlight=None):
        """绘制当前盘面的数字，highlight 为高亮位置"""
        for r in range(9):
            for c in range(9):
                num = self.current_grid[r][c]
                if num != 0:
                    color = BLACK
                    if self.puzzle[r][c] != 0:
                        color = BLUE  # 原始题目
                    elif highlight and (r, c) == highlight:
                        color = RED   # 正在填入
                    else:
                        color = GREEN # 已解出
                    
                    text = self.font.render(str(num), True, color)
                    x = 50 + c * 50 + 15
                    y = 50 + r * 50 + 10
                    self.screen.blit(text, (x, y))
    
    def run_solve_animation(self):
        """
        逐帧展示求解过程 —— 核心可视化
        每步等待一定时间，让观众看清数字如何填入
        """
        # 预先用回溯法收集所有步骤
        self.steps = []
        self._solve_collect_steps(self.current_grid.copy())
        
        step_idx = 0
        while self.running and step_idx < len(self.steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            row, col, num, action = self.steps[step_idx]
            if action == "place":
                self.current_grid[row][col] = num
            elif action == "remove":
                self.current_grid[row][col] = 0
            
            self.draw_grid()
            self.draw_numbers(highlight=(row, col))
            
            # 显示步骤信息
            info = self.small_font.render(
                f"Step {step_idx+1}/{len(self.steps)}: "
                f"{'填入' if action=='place' else '回溯'} ({row},{col})={num}",
                True, BLACK
            )
            self.screen.blit(info, (50, 520))
            
            pygame.display.flip()
            self.clock.tick(5)  # 每秒5步，可调节速度
            step_idx += 1
        
        # 完成后的保持
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.draw_grid()
            self.draw_numbers()
            done_text = self.font.render("求解完成！", True, RED)
            self.screen.blit(done_text, (200, 530))
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()
    
    def _solve_collect_steps(self, grid):
        """回溯求解并记录每一步操作（填入/回溯）"""
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    for num in range(1, 10):
                        if is_valid(grid, r, c, num):
                            grid[r][c] = num
                            self.steps.append((r, c, num, "place"))
                            if self._solve_collect_steps(grid):
                                return True
                            grid[r][c] = 0
                            self.steps.append((r, c, num, "remove"))
                    return False
        return True