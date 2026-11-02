"""공통 입력 처리 - 공백 제거, 숫자 변환, 범위, 빈 입력을 한곳에서 다룬다.

KeyboardInterrupt(Ctrl+C)와 EOFError(입력 끝)는 일부러 잡지 않고 위로 올려 보낸다.
최상위(main)에서 한 번에 받아 저장 후 안전하게 종료하기 위해서다.
"""
import re

_INT_PATTERN = re.compile(r"[+-]?\d+")


def read_int(prompt, low, high):
    """low~high 사이의 정수를 받을 때까지 다시 묻는다."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
            continue
        if not _INT_PATTERN.fullmatch(raw):
            print(f"⚠️ 숫자가 아닙니다 ('{raw}'). {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        value = int(raw)
        if not low <= value <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return value


def read_text(prompt, label="내용"):
    """공백을 뺀 뒤 비어 있지 않은 글자를 받을 때까지 다시 묻는다."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print(f"⚠️ {label}이(가) 비어 있습니다. 다시 입력하세요.")
