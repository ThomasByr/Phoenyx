import os

__all__ = ["warn"]


def move(y, x):
    """
    moves the cursor to the ``(y, x)`` location in the terminal
    """
    print("\033[%d;%dH" % (y, x))


def cls():
    """
    clears terminal, os independant
    """
    os.system("cls" if os.name == "nt" else "clear")


class ErrorHandler:
    """
    ErrorHandler
    ============
    An invisible class to handle warnings. Phoenyx uses it for warnings and soft errors.
    """
    def __init__(self) -> None:
        """
        new ErrorHangler instance
        """
        cls()
        print("Hello from Phoenyx")
        self.all_errors: dict[str, int] = dict()
        self.is_soft = True

    def warn(self, msg: str) -> None:
        """
        adds ``msg`` to the error log
        """
        try:
            self.all_errors[msg] += 1
        except KeyError:
            self.all_errors[msg] = 1

        if self.is_soft:
            self.display_all()
        else:
            print(msg, end="\n")

    def display_all(self) -> None:
        """
        display all errors
        """
        i = 1
        for k, v in self.all_errors.items():
            i += 1
            move(i, 0)
            print(f"\r{k} ({v})", end="", flush=True)


err = ErrorHandler()  # default for Phoenyx


def set_soft(flush: bool) -> None:
    """
    sets wether or not the errors are displayed the "pretty" way

    Parameters
    ----------
        flush : bool
            True means errors will not turn into spam
    """
    err.is_soft = flush


def warn(msg: str) -> None:
    """
    warns the user\\
    does not repeat previous warnings

    Parameters
    ----------
        msg : str
            the string that represent the message
    """
    err.warn(msg)
