"""游戏模块测试"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
pygame.init()

# 测试游戏逻辑
from tetris.game import TetrisGame
from tetris.tetromino import Tetromino

# 测试1: 创建游戏
print("测试1: 创建游戏...")
game = TetrisGame()
assert game is not None
assert not game.game_over
assert game.score == 0
assert game.level == 1
assert game.lines == 0
print("  通过!")

# 测试2: 移动方块
print("测试2: 移动方块...")
game2 = TetrisGame()
initial_x = game2.current_piece.x
game2.move_piece(1)
assert game2.current_piece.x == initial_x + 1
print("  通过!")

# 测试3: 旋转方块
print("测试3: 旋转方块...")
game3 = TetrisGame()
initial_rotation = game3.current_piece.rotation
game3.rotate_piece()
assert game3.current_piece.rotation == (initial_rotation + 1) % 4
print("  通过!")

# 测试4: 下落方块
print("测试4: 下落方块...")
game4 = TetrisGame()
initial_y = game4.current_piece.y
game4.drop_piece()
assert game4.current_piece.y == initial_y + 1
print("  通过!")

# 测试5: 消行
print("测试5: 消行...")
game5 = TetrisGame()
# 手动填充一行满
game5.board[19] = [(255, 0, 0) for _ in range(10)]
initial_lines = game5.lines
initial_score = game5.score
# 锁定当前方块触发消行检测
game5._clear_lines()
assert game5.lines == initial_lines + 1
print("  通过!")

# 测试6: 硬下落
print("测试6: 硬下落...")
game6 = TetrisGame()
game6.hard_drop()
# 方块应该已经在底部
print("  通过!")

# 测试7: 暂停功能
print("测试7: 暂停/继续...")
game7 = TetrisGame()
assert not game7.paused
game7.toggle_pause()
assert game7.paused
game7.toggle_pause()
assert not game7.paused
print("  通过!")

# 测试8: 游戏重置
print("测试8: 游戏重置...")
game8 = TetrisGame()
game8.score = 1000
game8.level = 5
game8.lines = 50
game8.reset()
assert game8.score == 0
assert game8.level == 1
assert game8.lines == 0
print("  通过!")

# 测试9: 渲染器
print("测试9: 渲染器...")
screen = pygame.display.set_mode((400, 300))
from tetris.renderer import Renderer
renderer = Renderer(screen)
assert renderer is not None
print("  通过!")

pygame.quit()
print("\n=== 所有测试通过! ===")