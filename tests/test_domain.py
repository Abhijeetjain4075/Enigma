import pytest

from enigma.domain import InvalidTransition, TransactionStatus, validate_transition


def test_happy_path_transitions_are_valid() -> None:
    pairs = [
        (TransactionStatus.CREATED, TransactionStatus.VALIDATED),
        (TransactionStatus.VALIDATED, TransactionStatus.AUTHORIZED),
        (TransactionStatus.AUTHORIZED, TransactionStatus.INITIATED),
        (TransactionStatus.INITIATED, TransactionStatus.ACTIVE),
        (TransactionStatus.ACTIVE, TransactionStatus.COMPLETED),
        (TransactionStatus.COMPLETED, TransactionStatus.BILLED),
        (TransactionStatus.BILLED, TransactionStatus.SETTLED),
    ]
    for source, target in pairs:
        validate_transition(source, target)


def test_impossible_transition_is_rejected() -> None:
    with pytest.raises(InvalidTransition):
        validate_transition(TransactionStatus.CREATED, TransactionStatus.SETTLED)


def test_refund_cannot_transition_before_billing() -> None:
    with pytest.raises(InvalidTransition):
        validate_transition(TransactionStatus.ACTIVE, TransactionStatus.REFUNDED)
