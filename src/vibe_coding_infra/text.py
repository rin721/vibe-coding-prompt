from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for raw in TOKEN_RE.findall(text):
        token = raw.lower()
        tokens.append(token)
        if _contains_cjk(token) and len(token) > 1:
            tokens.extend(token[index : index + 2] for index in range(len(token) - 1))
    return tokens


def _contains_cjk(value: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in value)


def chunk_text(text: str, max_chars: int = 1200, overlap: int = 120) -> list[str]:
    normalized = text.replace("\r\n", "\n")
    blocks = [block.strip() for block in re.split(r"\n{2,}", normalized) if block.strip()]
    chunks: list[str] = []
    current = ""

    for block in blocks:
        if not current:
            current = block
            continue
        if len(current) + len(block) + 2 <= max_chars:
            current = f"{current}\n\n{block}"
        else:
            chunks.extend(_split_large_block(current, max_chars, overlap))
            current = block

    if current:
        chunks.extend(_split_large_block(current, max_chars, overlap))

    return [chunk.strip() for chunk in chunks if chunk.strip()]


def _split_large_block(text: str, max_chars: int, overlap: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def stable_id(*parts: str) -> str:
    digest = hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()
    return digest[:16]


def hashed_vector(text: str, dimensions: int = 128) -> list[float]:
    counts = Counter(tokenize(text))
    vector = [0.0] * dimensions
    if not counts:
        return vector
    for token, count in counts.items():
        bucket = int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16) % dimensions
        vector[bucket] += 1.0 + math.log(count)
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    return sum(a * b for a, b in zip(left, right))


def make_snippet(text: str, query: str, size: int = 220) -> str:
    compact = normalize_space(text)
    terms = tokenize(query)
    index = -1
    lowered = compact.lower()
    for term in terms:
        index = lowered.find(term)
        if index >= 0:
            break
    if index < 0:
        return compact[:size]
    start = max(0, index - size // 3)
    end = min(len(compact), start + size)
    return compact[start:end]
