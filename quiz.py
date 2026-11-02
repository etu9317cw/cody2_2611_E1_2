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


def default_quizzes():
    """첫 실행(또는 데이터 복구) 때 쓰는 기본 퀴즈. 주제: 이번 달 과제 - Git · Python · Docker."""
    return [
        Quiz("Git에서 지금까지 바꾼 내용을 저장소 기록으로 남기는 명령은?",
             ["git add", "git commit", "git push", "git clone"], 2),
        Quiz("인터넷의 저장소를 내 컴퓨터에 통째로 복사해 오는 명령은?",
             ["git init", "git pull", "git clone", "git branch"], 3),
        Quiz("다른 브랜치에서 한 작업을 지금 브랜치로 합치는 명령은?",
             ["git merge", "git status", "git log", "git diff"], 1),
        Quiz("터미널에서 지금 있는 폴더의 경로를 보여 주는 명령은?",
             ["ls", "cd", "mkdir", "pwd"], 4),
        Quiz("Python에서 이름표(키)로 값을 찾는 자료형은?",
             ["list", "dict", "bool", "int"], 2),
        Quiz("Docker 이미지를 실행하면 만들어지는 '실행 중인 상자'는?",
             ["이미지", "레지스트리", "컨테이너", "볼륨"], 3),
        Quiz("docker run -p 8080:80 에서 8080은 무엇인가?",
             ["내 컴퓨터(호스트)의 포트 번호", "컨테이너 안 프로그램의 포트 번호",
              "이미지 버전", "컨테이너 개수"], 1),
        Quiz("Python 클래스의 __init__ 메서드는 언제 실행되는가?",
             ["클래스를 지울 때", "객체가 만들어질 때", "파일을 닫을 때", "프로그램이 끝날 때"], 2),
    ]
