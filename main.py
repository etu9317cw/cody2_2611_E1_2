"""나만의 퀴즈 게임 - 진입점 (메뉴)"""
import json
import sys
from pathlib import Path

from inputs import read_int, read_text
from quiz import CHOICE_COUNT, Quiz, default_quizzes

WIDTH = 40
STATE_PATH = Path(__file__).with_name("state.json")
MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료"]


def setup_console():
    """파이프·리다이렉트에서도 한글과 이모지가 깨지지 않게 UTF-8로 맞춘다."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def save_state(state):
    """퀴즈 목록을 프로젝트 루트의 state.json에 UTF-8로 저장한다."""
    data = {"quizzes": [quiz.to_dict() for quiz in state["quizzes"]]}
    try:
        STATE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as error:
        print(f"⚠️ 저장하지 못했습니다: {error}")


def add_quiz(state):
    """문제·선택지 4개·정답 번호를 입력받아 퀴즈를 추가하고 저장한다."""
    print("📌 새로운 퀴즈를 추가합니다.")
    question = read_text("문제를 입력하세요: ", "문제")
    choices = [read_text(f"선택지 {i}: ", "선택지") for i in range(1, CHOICE_COUNT + 1)]
    answer = read_int(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
    state["quizzes"].append(Quiz(question, choices, answer))
    save_state(state)
    print("✅ 퀴즈가 추가되었습니다!")


def show_menu():
    print("=" * WIDTH)
    print("🎯 나만의 퀴즈 게임 🎯".center(WIDTH))
    print("=" * WIDTH)
    for number, name in enumerate(MENU_ITEMS, start=1):
        print(f"{number}. {name}")
    print("=" * WIDTH)


def play_quiz(quizzes):
    """모든 퀴즈를 순서대로 출제하고 (맞힌 수, 전체 수)를 돌려준다. 퀴즈가 없으면 None."""
    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
        return None
    total = len(quizzes)
    print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")
    print("-" * WIDTH)
    correct = 0
    for number, quiz in enumerate(quizzes, start=1):
        quiz.show(number)
        picked = read_int("정답 입력: ", 1, CHOICE_COUNT)
        if quiz.is_correct(picked):
            correct += 1
            print("✅ 정답입니다!")
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({quiz.choices[quiz.answer - 1]})입니다.")
        print("-" * WIDTH)
    score = round(correct / total * 100)
    print("=" * WIDTH)
    print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
    print("=" * WIDTH)
    return correct, total


def run_menu():
    state = {"quizzes": default_quizzes()}
    while True:
        show_menu()
        choice = read_int("선택: ", 1, len(MENU_ITEMS))
        if choice == len(MENU_ITEMS):
            print("👋 게임을 종료합니다.")
            return
        if choice == 1:
            play_quiz(state["quizzes"])
        elif choice == 2:
            add_quiz(state)
        else:
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
