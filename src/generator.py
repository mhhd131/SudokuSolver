import random
import numpy as np

def is_valid(grid, row, col, num):
    """检查在 (row, col) 填入 num 是否合法"""
    # 检查行
    if num in grid[row, :]:
        return False
    # 检查列
    if num in grid[:, col]:
        return False
    # 检查 3x3 宫
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in grid[start_row:start_row+3, start_col:start_col+3]:
        return False
    return True

def fill_grid(grid):
    """递归回溯填满整个数独矩阵"""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                # 随机打乱 1-9，确保每次生成不同盘面 [2]
                nums = random.sample(range(1, 10), 9)
                for num in nums:
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if fill_grid(grid):
                            return True
                        grid[row][col] = 0  # 回溯
                return False
    return True

def generate_full_grid():
    """生成一个完整的 9x9 数独解"""
    grid = np.zeros((9, 9), dtype=int)
    fill_grid(grid)
    return grid
def create_puzzle(full_grid, empty_count=40):
    """
    从完整数独中挖空生成谜题
    empty_count: 挖空数量（40=简单, 50=中等, 60=困难）
    """
    puzzle = full_grid.copy()
    # 随机选择 empty_count 个不重复位置
    positions = random.sample(
        [(r, c) for r in range(9) for c in range(9)],
        empty_count
    )
    for r, c in positions:
        puzzle[r][c] = 0
    return puzzle

def has_unique_solution(puzzle):
    """检查谜题是否有唯一解（进阶要求）"""
    solutions = []
    def solve_and_count(grid):
        if len(solutions) > 1:
            return
        # 找到第一个空格
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    for num in range(1, 10):
                        if is_valid(grid, r, c, num):
                            grid[r][c] = num
                            solve_and_count(grid)
                            grid[r][c] = 0
                    return
        solutions.append(grid.copy())
    
    solve_and_count(puzzle.copy())
    return len(solutions) == 1