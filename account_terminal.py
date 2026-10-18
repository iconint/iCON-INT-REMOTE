"""Terminal-based account manager.

Allows a user to view and update account balance and account information
(e.g. name, email) using raw input typed directly into the terminal.

Run directly with:
    python3 account_terminal.py
"""


class Account:
    """A simple bank-style account with a balance and basic info fields."""

    def __init__(self, name="", email="", balance=0.0):
        self.name = name
        self.email = email
        self.balance = float(balance)
        self.pending = None

    def deposit(self, amount):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        return self.balance

    def request_change(self, kind, amount):
        """Queue a balance change (deposit/withdraw) pending approval."""
        if kind not in ("deposit", "withdraw"):
            raise ValueError(f"Unknown balance change: {kind}")
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if kind == "withdraw" and amount > self.balance:
            raise ValueError("Insufficient balance")
        if self.pending is not None:
            raise ValueError("A change is already pending approval")
        self.pending = {"kind": kind, "amount": amount}
        return self.pending

    def approve(self):
        """Apply the pending balance change."""
        if self.pending is None:
            raise ValueError("No pending change to approve")
        kind, amount = self.pending["kind"], self.pending["amount"]
        self.pending = None
        if kind == "deposit":
            return self.deposit(amount)
        return self.withdraw(amount)

    def reject(self):
        """Discard the pending balance change."""
        if self.pending is None:
            raise ValueError("No pending change to reject")
        self.pending = None
        return self.balance

    def update_info(self, field, value):
        if field not in ("name", "email"):
            raise ValueError(f"Unknown account field: {field}")
        setattr(self, field, value)
        return getattr(self, field)

    def info(self):
        return {
            "name": self.name,
            "email": self.email,
            "balance": self.balance,
            "pending": self.pending,
        }


HELP_TEXT = """\
Available commands:
  balance                 Show current balance
  deposit <amount>        Request a deposit (requires approval)
  withdraw <amount>       Request a withdrawal (requires approval)
  approve                 Approve and apply the pending balance change
  reject                  Discard the pending balance change
  update <field> <value>  Update account info (name or email)
  info                    Show full account information
  help                    Show this help message
  quit                    Exit the terminal
"""


def run(account=None, input_func=input, output_func=print):
    """Read raw commands from the terminal and apply them to an account.

    ``input_func``/``output_func`` are injectable for testing/automation but
    default to the real terminal ``input``/``print``.
    """
    if account is None:
        account = Account()

    output_func("Account terminal ready. Type 'help' for commands.")
    while True:
        try:
            raw = input_func("> ")
        except EOFError:
            break

        raw = raw.strip()
        if not raw:
            continue

        parts = raw.split()
        command = parts[0].lower()

        try:
            if command == "quit" or command == "exit":
                break
            elif command == "help":
                output_func(HELP_TEXT)
            elif command == "balance":
                output_func(f"Balance: {account.balance}")
            elif command == "deposit":
                pending = account.request_change("deposit", parts[1])
                output_func(f"Pending deposit of {pending['amount']}. Type 'approve' or 'reject'.")
            elif command == "withdraw":
                pending = account.request_change("withdraw", parts[1])
                output_func(f"Pending withdrawal of {pending['amount']}. Type 'approve' or 'reject'.")
            elif command == "approve":
                new_balance = account.approve()
                output_func(f"Approved. New balance: {new_balance}")
            elif command == "reject":
                account.reject()
                output_func("Pending change rejected.")
            elif command == "update":
                field, value = parts[1], " ".join(parts[2:])
                new_value = account.update_info(field, value)
                output_func(f"Updated {field}: {new_value}")
            elif command == "info":
                output_func(account.info())
            else:
                output_func(f"Unknown command: {command}. Type 'help' for commands.")
        except (IndexError, ValueError) as exc:
            output_func(f"Error: {exc}")

    return account


if __name__ == "__main__":
    run()
