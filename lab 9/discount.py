
from abc import ABC, abstractmethod


# Strategy pattern: every discount type is its own class with the same
# apply() method. Order just calls apply() and doesn't care which one it has.
class DiscountStrategy(ABC):

    @abstractmethod
    def apply(self, total: float) -> float:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass


class NoDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total

    def describe(self) -> str:
        return "No discount"


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage: float):
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")

        self.__percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)

    def describe(self) -> str:
        return f"{self.__percentage:g}% off"


class BulkDiscount(DiscountStrategy):

    def __init__(self, threshold: float, amount: float):
        if threshold < 0 or amount <= 0:
            raise ValueError("Threshold cannot be negative and amount "
                             "must be greater than zero.")

        self.__threshold: float = float(threshold)
        self.__amount: float = float(amount)

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            # don't let the total go below 0
            return max(total - self.__amount, 0.0)

        return total

    def describe(self) -> str:
        return (f"${self.__amount:.2f} off orders of "
                f"${self.__threshold:.2f} or more")


# Added for 2.4 - a new discount without touching the Order class at all
class StudentDiscount(DiscountStrategy):

    STUDENT_RATE = 5

    def apply(self, total: float) -> float:
        return total * (1 - self.STUDENT_RATE / 100)

    def describe(self) -> str:
        return f"Student discount ({self.STUDENT_RATE}% off)"
