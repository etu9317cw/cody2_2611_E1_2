"""나만의 퀴즈 게임 - 진입점 (메뉴)"""

WIDTH = 40
MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료"]


def show_menu():
    print("=" * WIDTH)
    print("🎯 나만의 퀴즈 게임 🎯".center(WIDTH))
    print("=" * WIDTH)
    for number, name in enumerate(MENU_ITEMS, start=1):
        print(f"{number}. {name}")
    print("=" * WIDTH)


def main():
    while True:
        show_menu()
        choice = input("선택: ").strip()
        if choice == "5":
            print("👋 게임을 종료합니다.")
            break
        if choice in ("1", "2", "3", "4"):
            print(f"[{MENU_ITEMS[int(choice) - 1]}] 기능은 아직 준비 중입니다.")
        else:
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    main()
