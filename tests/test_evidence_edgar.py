import json

import pandas as pd
import pytest

from usa_signal_bot.evidence.edgar import EdgarClient, RateLimiter, delisting_date, memberships_from_edgar
from usa_signal_bot.evidence.universe import PointInTimeUniverse

UA = "Test Research test@example.com"


class FakeNet:
    def __init__(self):
        self.calls = []
        self.tickers = {"0": {"cik_str": 1, "ticker": "AAA", "title": "A"}}
        self.subs = {
            1: {"filings": {"recent": {"form": ["10-K"], "filingDate": ["2020-01-01"]}}},
            2: {"filings": {"recent": {"form": ["8-K", "25-NSE", "15-12B"], "filingDate": ["2019-01-01", "2018-06-01", "2018-09-01"]}}},
        }

    def __call__(self, url, ua):
        assert ua == UA
        self.calls.append(url)
        if url.endswith("company_tickers.json"):
            return json.dumps(self.tickers).encode()
        return json.dumps(self.subs[int(url.rsplit("CIK", 1)[1][:10])]).encode()


def test_rate_limiter_enforces_gap_with_injected_clock():
    t = [0.0]
    sleeps = []
    lim = RateLimiter(10, clock=lambda: t[0], sleep=lambda s: (sleeps.append(s), t.__setitem__(0, t[0] + s)))
    for _ in range(11):
        lim.wait()
    assert t[0] == pytest.approx(1.0)  # 11 calls at 10/s need >= 1.0s
    with pytest.raises(ValueError):
        RateLimiter(11)


def test_user_agent_required(tmp_path, monkeypatch):
    monkeypatch.delenv("SEC_USER_AGENT", raising=False)
    with pytest.raises(ValueError):
        EdgarClient(tmp_path)


def test_cache_hit_avoids_network_and_stale_refetches(tmp_path):
    net, clock = FakeNet(), [1_000_000.0]
    c = EdgarClient(tmp_path, UA, RateLimiter(10, clock=lambda: 0.0, sleep=lambda s: None), net, max_age_days=1, now=lambda: clock[0])
    c.company_tickers()
    c.company_tickers()
    assert c.network_calls == 1
    import os
    for p in tmp_path.glob("*.json"):
        os.utime(p, (clock[0], clock[0]))
    clock[0] += 2 * 86400
    c.company_tickers()
    assert c.network_calls == 2


def test_only_sec_hosts(tmp_path):
    c = EdgarClient(tmp_path, UA, opener=FakeNet())
    with pytest.raises(ValueError):
        c.get_json("https://example.com/x.json")


def test_delisting_date_takes_earliest_form25():
    net = FakeNet()
    assert delisting_date(net.subs[2]) == pd.Timestamp("2018-06-01")
    assert delisting_date(net.subs[1]) is None


def test_memberships_frame_feeds_point_in_time_universe(tmp_path):
    c = EdgarClient(tmp_path, UA, RateLimiter(10, clock=lambda: 0.0, sleep=lambda s: None), FakeNet())
    frame, unresolved = memberships_from_edgar(c, [("AAA", None), ("DEAD", 2), ("ZZZ", None)], "2010-01-01")
    assert unresolved == ["ZZZ"]
    uni = PointInTimeUniverse.from_frame(frame)
    assert uni.members(pd.Timestamp("2015-01-01")) == ["AAA", "DEAD"]
    assert uni.members(pd.Timestamp("2019-01-01")) == ["AAA"]  # DEAD delisted 2018-06-01
