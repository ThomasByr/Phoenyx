import os

__all__ = ["warn", "error_console_set_soft", "error_console_load_soft"]


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
        print("Phoenyx -- errors console")
        move(2, 0)
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


err: ErrorHandler  # default for Phoenyx


def error_console_load_soft() -> None:
    """
    initializes Error Handeler\\
    very usefull for debuging
    """
    global err
    err = ErrorHandler()


def error_console_set_soft(flush: bool) -> None:
    """
    sets wether or not the errors are displayed the "pretty" way

    Parameters
    ----------
        flush : bool
            True means errors will not turn into spam
    """
    global err
    try:
        err.is_soft = flush
    except NameError:
        print(
            f"ERROR [error handler] : error handler is not running, you might consider adding ``error_handler_load_soft()`` in the previous line"
        )


def warn(msg: str) -> None:
    """
    warns the user\\
    does not repeat previous warnings if error handler has been initialized

    Parameters
    ----------
        msg : str
            the string that represent the message
    """
    global err
    try:
        err.warn(msg)
    except NameError:
        print(msg, end="\n")
