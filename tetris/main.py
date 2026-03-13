"""主程序入口"""
import sys
import pygame
from tetris.game import TetrisGame
from tetris.renderer import Renderer
from tetris.logger import logger


# 游戏状态
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"


class TetrisApp:
    """俄罗斯方块游戏应用"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("俄罗斯方块 - Tetris M25")

        # 创建窗口
        self.screen = pygame.display.set_mode(
            (Renderer.WINDOW_WIDTH, Renderer.WINDOW_HEIGHT)
        )

        self.renderer = Renderer(self.screen)
        self.game = None
        self.state = STATE_MENU
        self.clock = pygame.time.Clock()
        self.last_drop_time = 0

        logger.info("应用初始化完成")

    def run(self) -> None:
        """主循环"""
        logger.info("游戏主循环开始")

        running = True
        while running:
            # 事件处理
            running = self._handle_events()

            # 游戏逻辑更新
            if self.state == STATE_PLAYING:
                self._update_game()

            # 渲染
            self._render()

            # 控制帧率
            self.clock.tick(60)

        pygame.quit()
        logger.info("游戏退出")

    def _handle_events(self) -> bool:
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                return self._handle_keydown(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == STATE_MENU:
                    if self.renderer.get_start_button_rect().collidepoint(event.pos):
                        self._start_game()

        return True

    def _handle_keydown(self, key: int) -> bool:
        """处理按键事件"""
        if self.state == STATE_MENU:
            if key == pygame.K_RETURN or key == pygame.K_SPACE:
                self._start_game()
                return True

        elif self.state == STATE_PLAYING:
            if key == pygame.K_LEFT:
                self.game.move_piece(-1)
            elif key == pygame.K_RIGHT:
                self.game.move_piece(1)
            elif key == pygame.K_UP:
                self.game.rotate_piece()
            elif key == pygame.K_DOWN:
                self.game.drop_piece()
            elif key == pygame.K_SPACE:
                self.game.hard_drop()
            elif key == pygame.K_p:
                self.game.toggle_pause()
            elif key == pygame.K_ESCAPE:
                self.state = STATE_MENU
                logger.info("返回主菜单")

        elif self.state == STATE_GAME_OVER:
            if key == pygame.K_SPACE:
                self._start_game()
            elif key == pygame.K_ESCAPE:
                self.state = STATE_MENU

        return True

    def _update_game(self) -> None:
        """更新游戏状态"""
        if self.game is None or self.game.paused or self.game.game_over:
            return

        current_time = pygame.time.get_ticks()
        drop_interval = self.game.get_drop_speed()

        if current_time - self.last_drop_time >= drop_interval:
            self.game.drop_piece()
            self.last_drop_time = current_time

    def _render(self) -> None:
        """渲染界面"""
        if self.state == STATE_MENU:
            self.renderer.draw_menu()
        elif self.state == STATE_PLAYING or self.state == STATE_GAME_OVER:
            self.renderer.draw_game(self.game)

        pygame.display.flip()

    def _start_game(self) -> None:
        """开始新游戏"""
        self.game = TetrisGame()
        self.state = STATE_PLAYING
        self.last_drop_time = pygame.time.get_ticks()
        logger.info("开始新游戏")


def main():
    """主函数"""
    try:
        app = TetrisApp()
        app.run()
    except Exception as e:
        logger.error(f"游戏异常退出: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()