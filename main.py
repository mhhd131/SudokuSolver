from src.generator import generate_full_grid, create_puzzle
from src.visualizer import SudokuVisualizer

def main():
    print("正在生成完整数独...")
    full_grid = generate_full_grid()
    
    print("正在挖空生成谜题（中等难度，挖50个空）...")
    puzzle = create_puzzle(full_grid, empty_count=50)
    
    print("启动可视化求解器...")
    viz = SudokuVisualizer(puzzle, full_grid)
    viz.run_solve_animation()

if __name__ == "__main__":
    main()
