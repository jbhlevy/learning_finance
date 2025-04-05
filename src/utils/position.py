import numpy as np


class Position:
    def __init__(
        self,
        ticker: str,
        entry_price: float,
        side: str,
        entry_date: str,
        shares: float | None = None,
        amount: float | None = None,
    ):
        if shares is None and amount is None:
            raise ValueError("Please specify at least shares or amount")

        self.ticker = ticker
        self.entry_price = entry_price
        self.side = side  # 'long' or 'short'
        self.entry_date = entry_date

        if shares is not None and amount is not None:
            assert np.abs(shares * entry_price) == amount
            self.shares = shares
            self.amount = amount
        elif shares is not None and amount is None:
            self.amount = shares * entry_price
            self.shares = shares
        elif shares is None and amount is not None:
            self.shares = amount / entry_price
            self.amount = amount

        if side == "long" and self.shares < 0:
            print(
                "Position is long but shares were negative, switeched them to positive"
            )
            self.shares *= -1
        if side == "short" and self.shares > 0:
            print(
                "Position is short but shares are positive, swicthed them to negative"
            )
            self.shares *= -1

        self.exit_price = None
        self.exit_date = None

    def close(self, exit_price, exit_date):
        self.exit_price = exit_price
        self.exit_date = exit_date

    def pnl(self):
        if self.exit_price is None:
            return None  # Not closed yet
        return self.shares * (self.exit_price - self.entry_price)

    def close_and_compute_pnl(self, exit_price, exit_date):
        self.close(exit_price=exit_price, exit_date=exit_date)
        return self.pnl()

    def is_open(self):
        return self.exit_price is None

    def __repr__(self):
        status = "OPEN" if self.is_open() else "CLOSED"
        return (
            f"<{self.side.upper()} {self.ticker} | {self.shares:.2f} shares | {status}>"
        )


if __name__ == "__main__":
    # Test for the position class
    position1 = Position(
        "AAPL", entry_price=100, side="long", entry_date="today", amount=50
    )
    position2 = Position(
        "MSFT", entry_price=200, side="short", entry_date="today", shares=0.2
    )

    pnl1 = position1.close_and_compute_pnl(exit_price=150, exit_date="tomorrow")
    pnl1_ = position1.close_and_compute_pnl(exit_price=50, exit_date="tomorrow")

    pnl2 = position2.close_and_compute_pnl(exit_price=150, exit_date="tomorrow")
    pnl2_ = position2.close_and_compute_pnl(exit_price=250, exit_date="tomorrow")
    print(position1)
    print("long stock")
    print(pnl1)
    print(pnl1_)
    print("short stock")
    print(pnl2)
    print(pnl2_)
