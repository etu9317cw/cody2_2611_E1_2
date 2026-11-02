"""나만의 퀴즈 게임 - 진입점 (메뉴)"""
import sys

from inputs import read_int

WIDTH = 40
MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료"]


def setup_console():
    """파이프·리다이렉트에서도 한글과 이모지가 깨지지 않게 UTF-8로 맞춘다."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def show_menu():
    print("=" * WIDTH)
    print("🎯 나만의 퀴즈 게임 🎯".center(WIDTH))
    print("=" * WIDTH)
    for number, name in enumerate(MENU_ITEMS, start=1):
        print(f"{number}. {name}")
    print("=" * WIDTH)


def run_menu():
    while True:
        show_menu()
        choice = read_int("선택: ", 1, len(MENU_ITEMS))
        if choice == len(MENU_ITEMS):
            print("👋 게임을 종료합니다.")
            return
        print(f"[{MENU_ITEMS[choice - 1]}] 기능은 아직 준비 중입니다.")


def main():
    setup_console()
    try:
        run_menu()
    except (KeyboardInterrupt, EOFError):
        # 저장 로직은 파일 입출력 단계에서 여기에 연결한다.
        print("\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
