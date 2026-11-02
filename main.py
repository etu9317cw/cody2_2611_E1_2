"""나만의 퀴즈 게임 - 진입점. 실행: python main.py"""
import sys

from game import QuizGame


def setup_console():
    """파이프·리다이렉트에서도 한글과 이모지가 깨지지 않게 UTF-8로 맞춘다."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main():
    setup_console()
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n⚠️ 입력이 중단되었습니다. 저장 후 안전하게 종료합니다.")
        game.save()


if __name__ == "__main__":
    main()
