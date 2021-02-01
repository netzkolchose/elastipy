import re
import datetime

from helper import get_web_file



USERNAME = r"[a-zA-Z0-9_\-\|]+`?"

RE_LOG_FILE = re.compile(r'.*href="(setiquest\.[\d-]+\.log).*')

RE_LOG_LINES = [
    re.compile(r"\[([\d:pam]+)\]\s(.*)"),
    re.compile(r"([\d\-:T]+)\s(.*)"),
    re.compile(r"\(([\d\s:PAM]+)\)\s(.*)"),
]


RE_USER_EVENT = [
    {
        "re": re.compile(rf"^({USERNAME}) joined the chat room"),
        "user": 0,
        "event": "join",
    },
    {
        "re": re.compile(rf"^({USERNAME}) entered the room"),
        "user": 0,
        "event": "join",
    },
    {
        "re": re.compile(rf"({USERNAME}) joined #setiquest"),
        "user": 0,
        "event": "join",
    },
    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) has joined #setiquest"),
        "user": 0,
        "event": "join",
    },
    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) joined #setiquest"),
        "user": 0,
        "event": "join",
    },
    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) joined the chat room"),
        "user": 0,
        "event": "join",
    },
    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) returned to #setiquest"),
        "user": 0,
        "event": "join",
    },
    {
        "re": re.compile(rf"^({USERNAME}) left the chat room"),
        "user": 0,
        "event": "leave",
    },
    {
        "re": re.compile(rf"^({USERNAME}) left the room"),
        "user": 0,
        "event": "leave",
    },
    {
        "re": re.compile(rf"^({USERNAME}) has left the room"),
        "user": 0,
        "event": "leave",
    },
    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) has left #setiquest"),
        "user": 0,
        "event": "leave",
    },
    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) has quit IRC"),
        "user": 0,
        "event": "leave",
    },
    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) left irc:"),
        "user": 0,
        "event": "leave",
    },
    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) left #setiquest"),
        "user": 0,
        "event": "leave",
    },

    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) got netsplit"),
        "user": 0,
        "event": "net-split",
    },
    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) got lost in the net-split"),
        "user": 0,
        "event": "net-split",
    },

    {
        "re": re.compile(rf"^({USERNAME}) is now known as ({USERNAME})"),
        "user": 0,
        "event": "rename",
        "rename_to": 1,
    },
    {
        "re": re.compile(rf"^\*\*\* ({USERNAME}) is now known as ({USERNAME})"),
        "user": 0,
        "event": "rename",
        "rename_to": 1,
    },
    {
        "re": re.compile(rf"^\*\*\* Nick change: ({USERNAME}) -> ({USERNAME})"),
        "user": 0,
        "event": "rename",
        "rename_to": 1,
    },

    {
        "re": re.compile(rf"^\*\*\*.*freenode\.net sets mode: (.*)"),
        "event": "set-mode",
        "mode": 0,
    },
    {
        "re": re.compile(rf"^#setiquest: mode change '(.*)'"),
        "event": "set-mode",
        "mode": 0,
    },

    # <username> does something
    {
        "re": re.compile(rf"^• ({USERNAME}) (.+)"),
        "user": 0,
        "user_event": 1,
    },
    {
        "re": re.compile(rf"^\*\*\*({USERNAME}) (.+)"),
        "user": 0,
        "user_event": 1,
    },
    {
        "re": re.compile(rf"^\* ({USERNAME}) (.*)"),
        "user": 0,
        "user_event": 1,
    },

    {
        "re": re.compile(r"^The topic for #setiquest is: (.*)"),
        "event": "set-topic",
        "topic": 0,
    },
    {
        "re": re.compile(r"^\*\*\* Topic changed on #setiquest by [^:]+: (.*)"),
        "event": "set-topic",
        "topic": 0,
    },
    {
        "re": re.compile(r"^The account has disconnected"),
        "event": "log-disconnect",
    },
    {
        "re": re.compile(r"^You left the chat by being disconnected from the server\."),
        "event": "log-disconnect",
    },
    {
        "re": re.compile(r"^Logging started\."),
        "event": "log-connect",
    },
    {
        "re": re.compile(r"^You rejoined the room\."),
        "event": "log-connect",
    },
    {
        "re": re.compile(rf"^({USERNAME}):\s(.*)"),
        "user": 0,
        "event": "write",
        "text": 1,
    },
    {
        "re": re.compile(rf"^<({USERNAME})>\s(.*)"),
        "user": 0,
        "event": "write",
        "text": 1,
    },
    {
        "re": re.compile(rf"^({USERNAME}):$"),
        "user": 0,
        "event": "write",
        "text": "",
    },
    {
        "re": re.compile(rf"^<({USERNAME})>$"),
        "user": 0,
        "event": "write",
        "text": "",
    },
    {
        "re": re.compile(rf".*\[freenode-info\] (.*)"),
        "event": "freenode-info",
        "text": 0,
    },
    # ignore time-stamps
    {
        "re": re.compile(r"^--- [A-Z][a-z][a-z] [A-Z][a-z]+\s+\d\d? \d{4}")
    },
    # ignore those:
    {
        "re": re.compile(r"^TS resync"),
    },
    {
        "re": re.compile(r"^\*\*\* Possible future nick collision")
    },
    {
        "re": re.compile(r".*Notice -- TS for #setiquest changed")
    },
    {
        "re": re.compile(r"^Last message repeated 1 time\(s\).$")
    },
]


DATE_FORMATS = [
    ("%Y-%m-%dT%H:%M:%S", 0),
    ("%H:%M", 0),
    ("%H:%Mam", 0),
    ("%H:%Mpm", 12),
    ("%H:%M:%S am", 0),
    ("%H:%M:%S pm", 12),
]

def iter_setiquest_irc_logs():
    """
    Generator for tuples of (datetime.date, text contents) for each
    setiquest irc log file.

    """
    for year in range(2010, 2015):
        index_url = f"http://irc.sigblips.com/setiQuest/{year}/"
        filename = get_web_file(index_url, f"setiquest/index-{year}.html")
        with open(filename) as fp:
            index_lines = fp.readlines()

        for index_line in index_lines:
            match = RE_LOG_FILE.match(index_line)
            if match:
                log_filename = match.groups()[0]
                filename = get_web_file(f"{index_url}{log_filename}", f"setiquest/{year}/{log_filename}")

                date = datetime.datetime.strptime(log_filename, "setiquest.%m-%d-%Y.log").date()

                for encoding in ("utf-8", "iso-8859-1"):
                    with open(filename, encoding=encoding) as fp:
                        try:
                            yield date, fp.read()
                            break
                        except UnicodeDecodeError:
                            pass


def iter_log_lines(date: datetime.date, content: str):
    """
    Generates tuples of (time-str, line text)
    """
    previous_line = None

    for line in content.splitlines():
        if not line.strip():
            continue

        match = None
        for RE in RE_LOG_LINES:
            match = RE.match(line)
            if match:
                break

        if match:
            if previous_line:
                yield tuple(previous_line)

            previous_line = [
                match.groups()[0].strip().lower(),
                match.groups()[1].strip(),
            ]

        elif not match:
            if not previous_line:
                raise ValueError(
                    f"Could not parse line @ {date}: '{line}'"
                )
            previous_line[1] += " " + line.strip()

    if previous_line:
        yield tuple(previous_line)


def iter_messages():
    """
    Generator for all irc messages
    :return: dict
    """
    for log_date, content in iter_setiquest_irc_logs():
        for line_idx, (time, line) in enumerate(iter_log_lines(log_date, content)):
            date = None
            for date_format, hour_offset in DATE_FORMATS:
                try:
                    time_date = datetime.datetime.strptime(time, date_format)
                    date = time_date.replace(
                        year=log_date.year,
                        month=log_date.month,
                        day=log_date.day,
                        hour=time_date.hour,
                    ) + datetime.timedelta(hours=hour_offset)
                    break
                except ValueError:
                    pass

            if not date:
                raise ValueError(f"Can not parse chat-time '{time}'")

            if date < datetime.datetime(2010, 1, 1):
                raise ValueError(f"Invalid date {date} at log_date {log_date}")

            data = {
                "index": line_idx,
                "timestamp": date,
                "raw_line": line,
            }
            parse_message(data)

            yield data


def parse_message(data: dict):
    line = data["raw_line"]

    for RE in RE_USER_EVENT:
        match = RE["re"].match(line)
        if match:
            for key, value in RE.items():
                if key != "re":
                    if isinstance(value, int):
                        data[key] = match.groups()[value]
                    else:
                        data[key] = value
            return

    # since we have this insane regexp compilation,
    #   everything must pass!
    raise ValueError(f"Can not determine user in '{data}'")


if __name__ == "__main__":
    for message in iter_messages():
        pass
