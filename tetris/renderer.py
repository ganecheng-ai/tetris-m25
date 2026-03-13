"""渲染模块 - 游戏界面绘制"""
import pygame
from typing import Tuple
from tetris.game import TetrisGame
from tetris.tetromino import Tetromino


# 颜色定义
COLORS = {
    'background': (30, 30, 40),
    'board_bg': (20, 20, 30),
    'grid': (40, 40, 50),
    'text': (255, 255, 255),
    'text_secondary': (180, 180, 180),
    'border': (100, 100, 150),
    'border_glow': (150, 150, 200),
    'button': (70, 70, 100),
    'button_hover': (90, 90, 130),
    'pause_overlay': (0, 0, 0, 150),
}


class Renderer:
    """游戏渲染器"""

    BLOCK_SIZE = 30  # 方块大小
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    SIDEBAR_WIDTH = 150  # 侧边栏宽度
    WINDOW_WIDTH = BOARD_WIDTH * BLOCK_SIZE + SIDEBAR_WIDTH + 40
    WINDOW_HEIGHT = BOARD_HEIGHT * BLOCK_SIZE + 80

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = None
        self.font_large = None
        self.font_small = None
        self._init_fonts()

    def _init_fonts(self):
        """初始化字体 - 优先使用系统字体"""
        # 尝试使用支持中文的字体
        try:
            # 尝试各种中文字体
            font_names = ['microsoftyahei', 'simhei', 'simsun', 'noto', 'wqy-zenhei', 'arial']
            for font_name in font_names:
                self.font = pygame.font.SysFont(font_name, 24)
                self.font_large = pygame.font.SysFont(font_name, 36)
                self.font_small = pygame.font.SysFont(font_name, 18)
                # 测试是否能渲染中文
                test_surface = self.font.render('测试', True, (255, 255, 255))
                if test_surface.get_width() > 0:
                    break
        except:
            pass

        # 如果没有找到中文字体，使用默认字体
        if self.font is None:
            self.font = pygame.font.Font(None, 24)
            self.font_large = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 18)

    def draw_game(self, game: TetrisGame) -> None:
        """绘制整个游戏界面"""
        # 绘制背景
        self.screen.fill(COLORS['background'])

        # 绘制游戏区域
        self._draw_board(game)

        # 绘制侧边栏
        self._draw_sidebar(game)

        # 绘制当前方块
        if game.current_piece and not game.game_over:
            self._draw_piece(game.current_piece)

        # 绘制暂停遮罩
        if game.paused:
            self._draw_pause_overlay()

        # 绘制游戏结束遮罩
        if game.game_over:
            self._draw_game_over_overlay(game)

    def _draw_board(self, game: TetrisGame) -> None:
        """绘制游戏区域"""
        board_x = 20
        board_y = 50

        # 绘制游戏区域背景
        board_rect = pygame.Rect(
            board_x - 2, board_y - 2,
            self.BOARD_WIDTH * self.BLOCK_SIZE + 4,
            self.BOARD_HEIGHT * self.BLOCK_SIZE + 4
        )
        pygame.draw.rect(self.screen, COLORS['border'], board_rect, 2)

        # 绘制网格背景
        bg_rect = pygame.Rect(
            board_x, board_y,
            self.BOARD_WIDTH * self.BLOCK_SIZE,
            self.BOARD_HEIGHT * self.BLOCK_SIZE
        )
        pygame.draw.rect(self.screen, COLORS['board_bg'], bg_rect)

        # 绘制网格线
        for i in range(self.BOARD_WIDTH + 1):
            x = board_x + i * self.BLOCK_SIZE
            pygame.draw.line(self.screen, COLORS['grid'], (x, board_y),
                           (x, board_y + self.BOARD_HEIGHT * self.BLOCK_SIZE), 1)
        for i in range(self.BOARD_HEIGHT + 1):
            y = board_y + i * self.BLOCK_SIZE
            pygame.draw.line(self.screen, COLORS['grid'], (board_x, y),
                           (board_x + self.BOARD_WIDTH * self.BLOCK_SIZE, y), 1)

        # 绘制已锁定方块
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                if game.board[y][x] != 0:
                    self._draw_block(
                        board_x + x * self.BLOCK_SIZE,
                        board_y + y * self.BLOCK_SIZE,
                        game.board[y][x]
                    )

    def _draw_piece(self, piece: Tetromino) -> None:
        """绘制当前方块"""
        board_x = 20
        board_y = 50

        blocks = piece.get_blocks()
        for bx, by in blocks:
            if by >= 0:  # 只绘制在游戏区域内的部分
                self._draw_block(
                    board_x + bx * self.BLOCK_SIZE,
                    board_y + by * self.BLOCK_SIZE,
                    piece.color
                )

    def _draw_block(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """绘制单个方块"""
        # 主体
        rect = pygame.Rect(x + 1, y + 1, self.BLOCK_SIZE - 2, self.BLOCK_SIZE - 2)
        pygame.draw.rect(self.screen, color, rect)

        # 高光效果
        highlight = pygame.Rect(x + 2, y + 2, self.BLOCK_SIZE - 4, 3)
        pygame.draw.rect(self.screen, (min(255, color[0] + 50),
                                        min(255, color[1] + 50),
                                        min(255, color[2] + 50)), highlight)

    def _draw_sidebar(self, game: TetrisGame) -> None:
        """绘制侧边栏"""
        board_x = 20 + self.BOARD_WIDTH * self.BLOCK_SIZE + 30
        board_y = 50

        # 绘制下一个方块区域
        next_label = self.font.render("下一个", True, COLORS['text'])
        self.screen.blit(next_label, (board_x, board_y))

        # 绘制下一个方块预览
        if game.next_piece:
            self._draw_preview_piece(game.next_piece, board_x + 30, board_y + 30)

        # 绘制分数
        score_y = board_y + 120
        score_label = self.font.render("分数", True, COLORS['text_secondary'])
        self.screen.blit(score_label, (board_x, score_y))
        score_value = self.font_large.render(str(game.score), True, COLORS['text'])
        self.screen.blit(score_value, (board_x, score_label.get_rect().bottom + 5))

        # 绘制等级
        level_y = score_y + 90
        level_label = self.font.render("等级", True, COLORS['text_secondary'])
        self.screen.blit(level_label, (board_x, level_y))
        level_value = self.font_large.render(str(game.level), True, COLORS['text'])
        self.screen.blit(level_value, (board_x, level_label.get_rect().bottom + 5))

        # 绘制行数
        lines_y = level_y + 90
        lines_label = self.font.render("行数", True, COLORS['text_secondary'])
        self.screen.blit(lines_label, (board_x, lines_y))
        lines_value = self.font_large.render(str(game.lines), True, COLORS['text'])
        self.screen.blit(lines_value, (board_x, lines_label.get_rect().bottom + 5))

        # 绘制操作说明
        help_y = board_y + 350
        help_texts = [
            "操作说明:",
            "← → 移动",
            "↑ 旋转",
            "↓ 软降",
            "空格 硬降",
            "P 暂停",
            "ESC 返回菜单"
        ]
        for i, text in enumerate(help_texts):
            help_surface = self.font_small.render(text, True, COLORS['text_secondary'])
            self.screen.blit(help_surface, (board_x, help_y + i * 22))

    def _draw_preview_piece(self, piece: Tetromino, x: int, y: int) -> None:
        """绘制方块预览"""
        blocks = piece.get_blocks()
        offset_x = min(bx for bx, _ in blocks)
        offset_y = min(by for _, by in blocks)

        for bx, by in blocks:
            px = x + (bx - offset_x) * (self.BLOCK_SIZE // 2)
            py = y + (by - offset_y) * (self.BLOCK_SIZE // 2)
            rect = pygame.Rect(px + 1, py + 1, self.BLOCK_SIZE // 2 - 2, self.BLOCK_SIZE // 2 - 2)
            pygame.draw.rect(self.screen, piece.color, rect)

    def _draw_pause_overlay(self) -> None:
        """绘制暂停遮罩"""
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLORS['pause_overlay'])
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font_large.render("游戏暂停", True, COLORS['text'])
        text_rect = pause_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)

        continue_text = self.font.render("按 P 继续", True, COLORS['text_secondary'])
        continue_rect = continue_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(continue_text, continue_rect)

    def _draw_game_over_overlay(self, game: TetrisGame) -> None:
        """绘制游戏结束遮罩"""
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render("游戏结束", True, (255, 50, 50))
        text_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(game_over_text, text_rect)

        score_text = self.font.render(f"最终得分: {game.score}", True, COLORS['text'])
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 10))
        self.screen.blit(score_text, score_rect)

        restart_text = self.font.render("按 空格键 重新开始", True, COLORS['text_secondary'])
        restart_rect = restart_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

    def draw_menu(self) -> None:
        """绘制菜单界面"""
        self.screen.fill(COLORS['background'])

        # 标题
        title = self.font_large.render("俄罗斯方块", True, COLORS['text'])
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # 副标题
        subtitle = self.font.render("Tetris M25", True, COLORS['text_secondary'])
        subtitle_rect = subtitle.get_rect(center=(self.WINDOW_WIDTH // 2, 140))
        self.screen.blit(subtitle, subtitle_rect)

        # 开始游戏按钮
        start_rect = pygame.Rect(self.WINDOW_WIDTH // 2 - 80, 200, 160, 50)
        pygame.draw.rect(self.screen, COLORS['button'], start_rect, border_radius=10)
        start_text = self.font.render("开始游戏", True, COLORS['text'])
        start_text_rect = start_text.get_rect(center=start_rect.center)
        self.screen.blit(start_text, start_text_rect)

        # 操作说明
        help_y = 300
        help_texts = [
            "操作说明:",
            "← →  左右移动",
            "↑     顺时针旋转",
            "↓     软降 (加快下落)",
            "空格   硬降 (直接落底)",
            "P     暂停/继续",
            "ESC   返回主菜单"
        ]
        for i, text in enumerate(help_texts):
            help_surface = self.font.render(text, True, COLORS['text_secondary'])
            self.screen.blit(help_surface, (self.WINDOW_WIDTH // 2 - 100, help_y + i * 28))

        # 版本信息
        version = self.font_small.render("v0.1.4", True, (80, 80, 100))
        self.screen.blit(version, (10, self.WINDOW_HEIGHT - 30))

    def get_start_button_rect(self) -> pygame.Rect:
        """获取开始游戏按钮区域"""
        return pygame.Rect(self.WINDOW_WIDTH // 2 - 80, 200, 160, 50)