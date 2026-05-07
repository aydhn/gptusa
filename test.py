import sys
with open('usa_signal_bot/paper/paper_store.py', 'a') as f:
    f.write('''
def read_paper_equity_snapshots_jsonl(path: Path) -> List[Dict[str, Any]]:
    return _read_jsonl(path)

def read_paper_trades_jsonl(path: Path) -> List[Dict[str, Any]]:
    return _read_jsonl(path)

def read_paper_positions_jsonl(path: Path) -> List[Dict[str, Any]]:
    return _read_jsonl(path)
''')
