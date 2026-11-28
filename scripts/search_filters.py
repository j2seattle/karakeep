#!/usr/bin/env python3
"""Turn a plain-words search into a Karakeep query with real filters (WISH-1390, Library search box).

Karakeep does not understand "this week". This helper finds date words in the text, replaces them with
`after:YYYY-MM-DD` (and `before:` where the words ask for it), and leaves every other word alone.
It also returns the mode to use: Hybrid for a sentence, keyword for a query that is only filters.
Reference implementation with tests, for the Command Center Library search box (lane CC ports it).
Date words are English, relative to a given "today" (default: the local date). `after:` and `before:` include the named day
(checked live 2026-11-28: a bookmark saved on 2026-11-24 is found by after:2026-11-24, not by after:2026-11-25). A week starts on Monday.

  python search_filters.py "immich things I bookmarked this week"
  python search_filters.py --test
"""
import datetime
import re
import sys

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
FILLER = {"bookmarked", "saved", "added", "new", "things", "stuff", "links", "link", "i", "about", "the", "a", "of"}


def _d(day):
    return day.isoformat()


def parse(text, today=None):
    today = today or datetime.date.today()
    q = " " + text.strip() + " "
    filters = []

    def take(pattern, make):
        nonlocal q
        m = re.search(pattern, q, re.I)
        if m:
            filters.extend(make(m))
            q = q[:m.start()] + " " + q[m.end():]

    take(r"\b(today)\b", lambda m: [f"after:{_d(today)}"])
    take(r"\b(yesterday)\b", lambda m: [f"after:{_d(today - datetime.timedelta(days=1))}", f"before:{_d(today - datetime.timedelta(days=1))}"])
    take(r"\bthis week\b", lambda m: [f"after:{_d(today - datetime.timedelta(days=today.weekday()))}"])
    take(r"\blast week\b", lambda m: [f"after:{_d(today - datetime.timedelta(days=today.weekday() + 7))}",
                                      f"before:{_d(today - datetime.timedelta(days=today.weekday() + 1))}"])
    take(r"\bthis month\b", lambda m: [f"after:{_d(today.replace(day=1))}"])
    take(r"\b(?:in |over |within )?(?:the )?(?:last|past) (\d{1,3}) days\b", lambda m: [f"after:{_d(today - datetime.timedelta(days=int(m.group(1))))}"])
    take(r"\b(?:in |over |within )?(?:the )?(?:last|past) (\d{1,2}) weeks?\b", lambda m: [f"after:{_d(today - datetime.timedelta(days=7 * int(m.group(1))))}"])
    take(r"\b(?:since|after) (\d{4}-\d{2}-\d{2})\b", lambda m: [f"after:{m.group(1)}"])
    take(r"\bbefore (\d{4}-\d{2}-\d{2})\b", lambda m: [f"before:{m.group(1)}"])
    take(r"\brecently\b", lambda m: [f"after:{_d(today - datetime.timedelta(days=15))}"])
    words = [w for w in q.split() if w.lower() not in FILLER or w.startswith(("#", "is:"))]
    rest = " ".join(words)
    only_filters = not re.sub(r"(\S+:\S+|#\S+)", "", rest).strip()
    mode = "fts" if (only_filters or len(re.sub(r"(\S+:\S+|#\S+)", "", rest).split()) <= 1) else "hybrid"
    return {"query": " ".join(filter(None, [rest] + filters)), "mode": mode, "date_filters": filters}


def _test():
    t = datetime.date(2026, 11, 28)  # a Saturday
    cases = [
        ("immich things I bookmarked this week", "immich after:2026-11-23", "fts"),
        ("local model for embeddings #github-repo", "local model for embeddings #github-repo", "hybrid"),
        ("papers saved in the last 7 days about retrieval", "papers retrieval after:2026-11-21", "hybrid"),
        ("anything from yesterday", "anything from after:2026-11-27 before:2026-11-27", "hybrid"),
        ("#agents since 2026-11-01", "#agents after:2026-11-01", "fts"),
        ("diagram tools this month", "diagram tools after:2026-11-01", "hybrid"),
    ]
    bad = 0
    for text, want, mode in cases:
        got = parse(text, t)
        ok = got["query"] == want and got["mode"] == mode
        bad += not ok
        print("PASS" if ok else "FAIL", repr(text), "->", repr(got["query"]), got["mode"], "" if ok else f"(wanted {want!r} {mode})")
    return bad


if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        sys.exit(1 if _test() else 0)
    print(parse(" ".join(sys.argv[1:])))
