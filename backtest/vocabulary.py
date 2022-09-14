from enum import Enum
from utils import get_instances


def members(cls):
    return list(cls.__members__.keys())


class Vocabulary(Enum):
    # maps an interval to a number of seconds
    class Interval(Enum):
        SECOND = SECONDS = 1
        MINUTE = MINUTES = 60
        HOUR = HOURS = 60 * MINUTE
        DAY = DAYS = 24 * HOUR
        WEEK = WEEKS = 7 * DAY
        MONTH = MONTHS = 30 * DAY
        YEAR = YEARS = 365 * DAY

    Line = Enum("Line", get_instances("lines", upper=True))
    Event = Enum("Event", get_instances("events", upper=True))
    Transaction = Enum("Transaction", get_instances("transactions", upper=True))

    @classmethod
    def wordlist(cls):
        lst = []
        for member in members(cls):
            subcls = getattr(cls, member).value
            lst += members(subcls)
        return lst

    @classmethod
    def get_category(cls, word):
        for member in members(cls):
            if word in getattr(cls, member).value.__members__:
                return member
        return None

    @classmethod
    def str_to_enum(cls, word):
        cat = Vocabulary.get_category(cls, word)
        if cat:
            enum_cls = getattr(cls, cat).value
            element = getattr(enum_cls, word.upper())
            return element
        else:
            return None

    # TODO: Check somewhere for bad inputs
    @classmethod
    def parse_cmd(cmd):

        words = cmd.split(" ")

        enums = list(map(Vocabulary.str_to_enum, words))

        categories = list(map(type, enums))

        lines = []

        # TODO: add support for conjunctions as first thing to check for

        events = list(map(lambda cat: cat == Vocabulary.Event.value, categories))

        assert any(events), "Invalid cmd - Must include an Event"

        event_idx = events.index(True)

        lines.append(slice(0, event_idx))
        lines.append(slice(event_idx + 1))

        lines_data = []
        for line in lines:
            line_enums = enums[line]
            line_categories = categories[line]

            assert (
                line_categories[-1] == Vocabulary.Line.value
            ), "Invalid cmd - Clauses must end with a type of Line"

            line_type = line_enums[-1]

            line_data = line_type(line_enums[:-1])
            lines_data.append(line_data)

            # # TODO: Call a function inside line module
            # if line_type == Vocabulary.Line.SPOT:
            #     pass
            # elif line_type == Vocabulary.Line.SMA:
            #     pass
            # elif line_type == Vocabulary.Line.VWAP:
            #     pass
