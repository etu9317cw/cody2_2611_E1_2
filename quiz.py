"""퀴즈 한 문제를 표현하는 Quiz 클래스"""

CHOICE_COUNT = 4


class Quiz:
    """문제(question), 선택지 4개(choices), 정답 번호 1~4(answer)를 가진다."""

    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제가 비어 있습니다.")
        if (not isinstance(choices, list) or len(choices) != CHOICE_COUNT
                or not all(isinstance(c, str) and c.strip() for c in choices)):
            raise ValueError(f"선택지는 비어 있지 않은 {CHOICE_COUNT}개여야 합니다.")
        if isinstance(answer, bool) or not isinstance(answer, int) \
                or not 1 <= answer <= CHOICE_COUNT:
            raise ValueError(f"정답은 1~{CHOICE_COUNT} 사이 번호여야 합니다.")
        self.question = question.strip()
        self.choices = [c.strip() for c in choices]
        self.answer = answer

    def show(self, number=None):
        """문제와 선택지를 출력한다. number를 주면 '[문제 n]' 머리를 붙인다."""
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, picked):
        """사용자가 고른 번호가 정답이면 True."""
        return picked == self.answer
