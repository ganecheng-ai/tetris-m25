"""游戏核心逻辑模块"""
import random
from typing import List, Tuple, Optional
from tetris.tetromino import Tetromino, TETROMINO_SHAPES, TETROMINO_COLORS
from tetris.logger import logger


class TetrisGame:
    """俄罗斯方块游戏类"""

    # 游戏区域大小
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20

    def __init__(self):
        self.board: List[List[int]] = self._create_empty_board()
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.paused = False

        # 随机数生成器
        self.rng = random.Random()

        # 初始化第一个方块
        self._spawn_piece()
        logger.info("游戏初始化完成")

    def _create_empty_board(self) -> List[List[int]]:
        """创建空的游戏区域"""
        return [[0 for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]

    def _spawn_piece(self) -> None:
        """生成新方块"""
        # 如果没有下一个方块，生成一个
        if self.next_piece is None:
            self.next_piece = self._create_random_piece()

        # 当前方块变为下一个方块
        self.current_piece = self.next_piece
        self.next_piece = self._create_random_piece()

        # 设置初始位置 (居中)
        self.current_piece.x = self.BOARD_WIDTH // 2 - 2
        self.current_piece.y = 0

        # 检查游戏是否结束
        if self._check_collision(self.current_piece):
            self.game_over = True
            logger.info("游戏结束!")

        logger.debug(f"生成新方块: {self.current_piece.type}")

    def _create_random_piece(self) -> Tetromino:
        """创建随机方块"""
        shape_types = list(TETROMINO_SHAPES.keys())
        shape_type = self.rng.choice(shape_types)
        return Tetromino(shape_type)

    def _check_collision(self, piece: Tetromino, dx: int = 0, dy: int = 0) -> bool:
        """检查方块是否与边界或其他方块碰撞"""
        blocks = piece.get_blocks()
        for bx, by in blocks:
            # 检查边界
            new_x = bx + dx
            new_y = by + dy
            if new_x < 0 or new_x >= self.BOARD_WIDTH:
                return True
            if new_y >= self.BOARD_HEIGHT:
                return True
            # 检查与其他方块碰撞
            if new_y >= 0 and self.board[new_y][new_x] != 0:
                return True
        return False

    def move_piece(self, dx: int) -> bool:
        """移动方块"""
        if self.current_piece is None or self.game_over or self.paused:
            return False

        if not self._check_collision(self.current_piece, dx, 0):
            self.current_piece.x += dx
            logger.debug(f"方块移动: dx={dx}, 位置=({self.current_piece.x}, {self.current_piece.y})")
            return True
        return False

    def rotate_piece(self) -> bool:
        """旋转方块"""
        if self.current_piece is None or self.game_over or self.paused:
            return False

        # 保存当前旋转状态
        old_rotation = self.current_piece.rotation
        old_x = self.current_piece.x

        # 尝试旋转
        self.current_piece.rotate()

        # 如果旋转后碰撞，尝试左右移动来适应
        if self._check_collision(self.current_piece):
            # 尝试向左移动
            self.current_piece.x -= 1
            if self._check_collision(self.current_piece):
                self.current_piece.x += 2  # 尝试向右移动
                if self._check_collision(self.current_piece):
                    # 恢复原状
                    self.current_piece.x = old_x
                    self.current_piece.rotation = old_rotation
                    return False

        logger.debug(f"方块旋转: {self.current_piece.type}, rotation={self.current_piece.rotation}")
        return True

    def drop_piece(self) -> bool:
        """下落方块一步"""
        if self.current_piece is None or self.game_over or self.paused:
            return False

        if not self._check_collision(self.current_piece, 0, 1):
            self.current_piece.y += 1
            return True
        else:
            # 方块落地，锁定到游戏区域
            self._lock_piece()
            return False

    def hard_drop(self) -> int:
        """硬下落 - 方块直接落到底部"""
        if self.current_piece is None or self.game_over or self.paused:
            return 0

        drop_distance = 0
        while not self._check_collision(self.current_piece, 0, 1):
            self.current_piece.y += 1
            drop_distance += 1

        self._lock_piece()
        logger.info(f"硬下落距离: {drop_distance}")
        return drop_distance

    def _lock_piece(self) -> None:
        """锁定方块到游戏区域"""
        if self.current_piece is None:
            return

        blocks = self.current_piece.get_blocks()
        for bx, by in blocks:
            if by >= 0:  # 忽略还在边界上方的方块
                self.board[by][bx] = self.current_piece.color

        logger.debug(f"方块锁定: {self.current_piece.type}")

        # 消除行
        self._clear_lines()

        # 生成新方块
        self._spawn_piece()

    def _clear_lines(self) -> None:
        """消除满行"""
        lines_cleared = 0
        new_board = []
        for row in self.board:
            if all(cell != 0 for cell in row):
                # 该行已满，消除它
                lines_cleared += 1
            else:
                # 保留该行
                new_board.append(row)

        if lines_cleared > 0:
            # 在顶部添加空行
            for _ in range(lines_cleared):
                new_board.insert(0, [0 for _ in range(self.BOARD_WIDTH)])
            self.board = new_board

            # 计算分数
            # 1行: 100, 2行: 300, 3行: 500, 4行: 800 * 等级
            line_scores = [0, 100, 300, 500, 800]
            self.score += line_scores[lines_cleared] * self.level
            self.lines += lines_cleared

            # 等级提升 (每10行升一级)
            new_level = self.lines // 10 + 1
            if new_level > self.level:
                self.level = new_level
                logger.info(f"升级! 当前等级: {self.level}")

            logger.info(f"消除 {lines_cleared} 行, 得分: {line_scores[lines_cleared] * self.level}")

    def toggle_pause(self) -> None:
        """切换暂停状态"""
        self.paused = not self.paused
        logger.info(f"游戏 {'暂停' if self.paused else '继续'}")

    def reset(self) -> None:
        """重置游戏"""
        self.board = self._create_empty_board()
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.paused = False
        self._spawn_piece()
        logger.info("游戏重置")

    def get_drop_speed(self) -> int:
        """获取下落速度 (毫秒)"""
        # 基础速度1000ms，每级减少50ms，最小100ms
        return max(100, 1000 - (self.level - 1) * 100)

    def get_ghost_y(self) -> int:
        """获取幽灵方块的y坐标（方块落下后的位置）"""
        if self.current_piece is None:
            return 0

        ghost_y = self.current_piece.y
        while not self._check_collision(self.current_piece, 0, ghost_y - self.current_piece.y + 1):
            ghost_y += 1
        return ghost_y