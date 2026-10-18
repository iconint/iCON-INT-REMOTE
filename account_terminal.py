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

    def update_info(self, field, value):
        if field not in ("name", "email"):
            raise ValueError(f"Unknown account field: {field}")
        setattr(self, field, value)
        return getattr(self, field)

    def info(self):
        return {"name": self.name, "email": self.email, "balance": self.balance}


HELP_TEXT = """\
Available commands:
  balance                 Show current balance
  deposit <amount>        Add funds to the account
  withdraw <amount>       Remove funds from the account
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
                new_balance = account.deposit(parts[1])
                output_func(f"Deposited. New balance: {new_balance}")
            elif command == "withdraw":
                new_balance = account.withdraw(parts[1])
                output_func(f"Withdrew. New balance: {new_balance}")
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
