"""豆瓣 API 示例（Douban API in Python）。

  python main.py search 小王子 --out items.csv                     # 按关键词搜书影音条目 / search items
  python main.py comments "<条目链接>" --out comments.csv          # 条目短评 / short comments
  python main.py reviews "<条目链接>" --limit 3 --out reviews.json # 条目长评，只要 3 条 / 3 long reviews
  python main.py topic "<小组话题链接>" --out topic.json           # 小组话题和回复 / group topic
"""
import argparse

from everyinfra import fetch, report

TYPES = ["all", "book", "movie", "music"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜条目 / search books, movies and music")
    s.add_argument("keyword")
    s.add_argument("--type", choices=TYPES, help="条目类型 / item type")
    c = sub.add_parser("comments", help="条目短评 / short comments of one item")
    c.add_argument("url")
    r = sub.add_parser("reviews", help="条目长评 / long reviews of one item")
    r.add_argument("url")
    r.add_argument("--limit", type=int, help="要几条，每条算一次调用 / rows to fetch, one call each")
    t = sub.add_parser("topic", help="小组话题和回复 / one group topic with replies")
    t.add_argument("url")
    for x in (s, c, r, t):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        params = {"keyword": a.keyword, **({"type": a.type} if a.type else {})}
        rows, charged = fetch("search", params)
    elif a.cmd == "comments":
        rows, charged = fetch("comments", {"url": a.url})
    elif a.cmd == "reviews":
        params = {"url": a.url, **({"limit": a.limit} if a.limit else {})}
        rows, charged = fetch("reviews", params)
    else:
        rows, charged = fetch("group_topic", {"url": a.url})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
