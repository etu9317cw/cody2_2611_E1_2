"""게임 전체를 관리하는 QuizGame 클래스"""
import json
import os
from pathlib import Path

from inputs import read_int, read_text
from quiz import CHOICE_COUNT, Quiz, default_quizzes

WIDTH = 40
STATE_PATH = Path(__file__).with_name("state.json")
MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료"]


class QuizGame:
    """퀴즈 목록과 최고 점수를 들고, 메뉴·풀기·추가·목록·점수·저장을 맡는다."""

    def __init__(self, state_path=STATE_PATH):
        self.state_path = Path(state_path)
        self.quizzes = default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None

    # ---- 저장 / 불러오기 ----
    def save(self):
        """퀴즈 목록과 최고 점수를 state.json에 UTF-8로 저장한다.

        임시 파일에 먼저 쓰고 바꿔치기해서, 쓰다가 끊겨도 기존 파일이 깨지지 않게 한다.
        """
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        temp_path = self.state_path.with_name(self.state_path.name + ".tmp")
        try:
            temp_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(temp_path, self.state_path)
        except OSError as error:
            print(f"⚠️ 저장하지 못했습니다: {error}")
            try:
                temp_path.unlink()
            except OSError:
                pass

    def reset_to_defaults(self):
        self.quizzes = default_quizzes()
        self.best_score = self.best_correct = self.best_total = None

    def load(self):
        """state.json을 읽는다. 없으면 기본 퀴즈, 손상되었으면 안내 후 기본 퀴즈로 복구한다."""
        if not self.state_path.exists():
            print("ℹ️ 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            return
        try:
            text = self.state_path.read_text(encoding="utf-8-sig")
            quizzes, best = self._parse_state(json.loads(text))
        except (OSError, ValueError) as error:  # JSON 문법·인코딩·형식 오류는 모두 ValueError 계열
            print(f"⚠️ 저장 파일을 읽지 못했습니다 ({error}). 기본 퀴즈로 복구합니다.")
            self.reset_to_defaults()
            return
        self.quizzes = quizzes
        self.best_score, self.best_correct, self.best_total = best
        detail = f"{self.best_score}점" if self.best_score is not None else "없음"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {detail})")

    @staticmethod
    def _parse_state(data):
        """읽은 JSON을 끝까지 검사한 뒤 (퀴즈 목록, (최고점수, 정답 수, 전체 수))로 돌려준다."""
        if not isinstance(data, dict):
            raise ValueError("최상위가 객체가 아닙니다")
        if not isinstance(data.get("quizzes"), list):
            raise ValueError("quizzes 목록이 없습니다")
        quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]

        def optional_int(key, low, high):
            value = data.get(key)
            if value is None:
                return None
            if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
                raise ValueError(f"{key} 값이 올바르지 않습니다")
            return value

        score = optional_int("best_score", 0, 100)
        correct = optional_int("best_correct", 0, 10_000)
        total = optional_int("best_total", 1, 10_000)
        if correct is not None and total is not None and correct > total:
            raise ValueError("best_correct가 best_total보다 큽니다")
        return quizzes, (score, correct, total)

    # ---- 화면 ----
    def show_menu(self):
        print("=" * WIDTH)
        print("🎯 나만의 퀴즈 게임 🎯".center(WIDTH))
        print("=" * WIDTH)
        for number, name in enumerate(MENU_ITEMS, start=1):
            print(f"{number}. {name}")
        print("=" * WIDTH)

    # ---- 기능 ----
    def play(self):
        """모든 퀴즈를 순서대로 출제한다. 끝나면 최고 점수를 비교·갱신한다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return
        total = len(self.quizzes)
        print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")
        print("-" * WIDTH)
        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.show(number)
            picked = read_int("정답 입력: ", 1, CHOICE_COUNT)
            if quiz.is_correct(picked):
                correct += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 "
                      f"({quiz.choices[quiz.answer - 1]})입니다.")
            print("-" * WIDTH)
        score = round(correct / total * 100)
        print("=" * WIDTH)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.update_best_score(correct, total):
            print("🎉 새로운 최고 점수입니다!")
        print("=" * WIDTH)

    def update_best_score(self, correct, total):
        """이번 점수가 최고 점수보다 높으면 갱신하고 저장한다. 갱신했으면 True."""
        score = round(correct / total * 100)
        if self.best_score is not None and score <= self.best_score:
            return False
        self.best_score, self.best_correct, self.best_total = score, correct, total
        self.save()
        return True

    def add_quiz(self):
        """문제·선택지 4개·정답 번호를 입력받아 퀴즈를 추가하고 저장한다."""
        print("📌 새로운 퀴즈를 추가합니다.")
        question = read_text("문제를 입력하세요: ", "문제")
        choices = [read_text(f"선택지 {i}: ", "선택지") for i in range(1, CHOICE_COUNT + 1)]
        answer = read_int(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        """등록된 퀴즈의 번호와 문제를 보여 준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * WIDTH)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * WIDTH)

    def show_score(self):
        """최고 점수를 보여 준다. 아직 풀지 않았으면 안내한다."""
        if self.best_score is None:
            print("ℹ️ 아직 퀴즈를 푼 기록이 없습니다. 먼저 퀴즈를 풀어 보세요.")
            return
        line = f"🏆 최고 점수: {self.best_score}점"
        if self.best_total is not None and self.best_correct is not None:
            line += f" ({self.best_total}문제 중 {self.best_correct}문제 정답)"
        print(line)

    # ---- 메인 루프 ----
    def run(self):
        self.load()
        actions = {1: self.play, 2: self.add_quiz, 3: self.list_quizzes, 4: self.show_score}
        while True:
            self.show_menu()
            choice = read_int("선택: ", 1, len(MENU_ITEMS))
            if choice == len(MENU_ITEMS):
                self.save()
                print("👋 게임을 종료합니다.")
                return
            actions[choice]()
