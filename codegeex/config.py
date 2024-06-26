from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, Tuple, Union

import torch
from transformers import PreTrainedModel

from codegeex.tokenizers import Tokenizer


class Config(ABC):
    def __init__(
        self,
        name: str,
        steps: int,
        sequence_length: int,
        micro_batch_size: int,
        gradient_accumulation_steps: int,
        padded_vocab_size: int,
        tokenizer: Tokenizer,
    ):
        self.name = name
        self.steps = steps
        self.sequence_length = sequence_length
        self.micro_batch_size = micro_batch_size
        self.gradient_accumulation_steps = gradient_accumulation_steps
        self.padded_vocab_size = padded_vocab_size
        self.tokenizer = tokenizer
        assert self.padded_vocab_size >= self.tokenizer.vocab_size()

    @abstractmethod
    def model(self) -> Union[torch.nn.Module, PreTrainedModel]:
        pass

    @abstractmethod
    def optimizer(self, model: torch.nn.Module) -> torch.optim.Optimizer:
        pass

    @abstractmethod
    def lr_scheduler(
        self, optimizer: torch.optim.Optimizer
    ) -> torch.optim.lr_scheduler._LRScheduler:
        pass

    @abstractmethod
    def random_input(
        self, device: torch.device
    ) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
        pass

    @abstractmethod
    def dataloader(
        self, device: torch.device
    ) -> Iterable[Tuple[Tuple[Any, ...], Dict[str, Any]]]:
        pass

    @property
    def tokens_per_batch(self) -> int:
        return (
            self.micro_batch_size
            * self.gradient_accumulation_steps
            * self.sequence_length
        )
