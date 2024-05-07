"""
A collection of classes for tokenization and tokenizers.
"""

from abc import ABC, abstractmethod
from typing import List

from tiktoken import Encoding as TiktokenTokenizer
from tokengeex import Tokenizer as TokenGeeXTokenizer


class Tokenizer(ABC):
    @abstractmethod
    def encode(self, text: str, include_special_tokens: bool = True) -> List[int]:
        pass

    @abstractmethod
    def encode_batch(
        self, texts: list, include_special_tokens: bool = True
    ) -> List[List[int]]:
        pass

    @abstractmethod
    def decode(self, tokens: List[int]) -> str:
        pass

    @abstractmethod
    def decode_batch(self, tokens: List[List[int]]) -> List[str]:
        pass

    @abstractmethod
    def vocab_size(self) -> int:
        pass

    @abstractmethod
    def special_tokens(self) -> List[str]:
        pass

    @abstractmethod
    def add_special_tokens(self, tokens: List[str]):
        pass

    @abstractmethod
    def token_to_id(self, token: bytes) -> int | None:
        pass

    @abstractmethod
    def id_to_token(self, id: int) -> bytes | None:
        pass

    @abstractmethod
    def special_token_to_id(self, token: str) -> int | None:
        pass

    @abstractmethod
    def id_to_special_token(self, id: int) -> str | None:
        pass


class WrappedTokenGeeXTokenizer(Tokenizer):
    def __init__(self, tokenizer: TokenGeeXTokenizer):
        self.tokenizer = tokenizer

    def encode(self, text: str, include_special_tokens: bool = True) -> List[int]:
        if include_special_tokens:
            return self.tokenizer.encode(text)
        return self.tokenizer.encode_ordinary(text)

    def encode_batch(
        self, texts: list, include_special_tokens: bool = True
    ) -> List[List[int]]:
        if include_special_tokens:
            return self.tokenizer.encode_batch(texts)
        return self.tokenizer.encode_ordinary_batch(texts)

    def decode(self, tokens: List[int], include_special_tokens: bool = False) -> str:
        return self.tokenizer.decode(tokens, include_special_tokens)

    def decode_batch(
        self, tokens: List[List[int]], include_special_tokens: bool = False
    ) -> List[str]:
        return self.tokenizer.decode_batch(tokens, include_special_tokens)

    def vocab_size(self) -> int:
        return self.tokenizer.vocab_size()

    def special_tokens(self) -> List[str]:
        return self.tokenizer.special_tokens()

    def add_special_tokens(self, tokens: List[str]):
        self.tokenizer.add_special_tokens(tokens)

    def token_to_id(self, token: bytes) -> int | None:
        return self.tokenizer.token_to_id(token)

    def id_to_token(self, id: int) -> bytes | None:
        token = self.tokenizer.id_to_token(id)
        if token is not None:
            (value, score) = token
            return value
        return None

    def special_token_to_id(self, token: str) -> int | None:
        return self.tokenizer.special_token_to_id(token)

    def id_to_special_token(self, id: int) -> str | None:
        return self.tokenizer.id_to_special_token(id)


class WrappedTiktokenTokenizer(Tokenizer):
    def __init__(self, tokenizer: TiktokenTokenizer):
        self.tokenizer = tokenizer

    def encode(self, text: str, include_special_tokens: bool = True) -> List[int]:
        if include_special_tokens:
            return self.tokenizer.encode(text)
        return self.tokenizer.encode_ordinary(text)

    def encode_batch(
        self, texts: list, include_special_tokens: bool = True
    ) -> List[List[int]]:
        if include_special_tokens:
            return self.tokenizer.encode_batch(texts)
        return self.tokenizer.encode_ordinary_batch(texts)

    def decode(self, tokens: List[int], include_special_tokens: bool = False) -> str:
        if include_special_tokens:
            raise NotImplementedError(
                "Tiktoken does not support decoding with special tokens."
            )
        return self.tokenizer.decode(tokens)

    def decode_batch(
        self, tokens: List[List[int]], include_special_tokens: bool = False
    ) -> List[str]:
        if include_special_tokens:
            raise NotImplementedError(
                "Tiktoken does not support decoding with special tokens."
            )
        return self.tokenizer.decode_batch(tokens)

    def vocab_size(self) -> int:
        return self.tokenizer.max_token_value + 1

    def special_tokens(self) -> List[str]:
        return list(self.tokenizer.special_tokens_set)

    def add_special_tokens(self, tokens: List[str]):
        raise NotImplementedError("Tiktoken does not support adding special tokens.")

    def token_to_id(self, token: bytes) -> int | None:
        return self.tokenizer.encode_single_token(token)

    def id_to_token(self, id: int) -> bytes | None:
        return self.tokenizer.decode_single_token_bytes(id)

    def special_token_to_id(self, token: str) -> int | None:
        return self.tokenizer.encode_single_token(token)

    def id_to_special_token(self, id: int) -> str | None:
        return self.tokenizer.decode_single_token_bytes(id).decode("utf-8")