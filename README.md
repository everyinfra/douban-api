# Douban API（豆瓣 API）

[English](#english) · [中文](#中文)

## English

This repo reads public Douban data with Python or curl. You can search books, movies, and music by keyword, read the short comments and long reviews of an item, and read a group topic with its replies. You need one EveryInfra API key. You do not need a Douban account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 4 capabilities cost $1.39 to $24.00 per 1,000 calls. Failed calls and empty results are not charged. The EveryInfra Douban API has 4 capabilities, all listed on the platform page: <https://everyinfra.com/en/douban-api?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

### Quick start

```bash
git clone https://github.com/everyinfra/douban-api.git
cd douban-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search 小王子 --out items.csv
python main.py comments "<item url>" --out comments.csv
python main.py reviews "<item url>" --limit 3 --out reviews.json
python main.py topic "<group topic url>" --out topic.json
```

- Take the item link from the `url` field of a `search` result, for example https://book.douban.com/subject/<ID>/. Movie and music items use the same kind of link.
- `reviews` is billed by the rows you ask for. `--limit 3` asks for 3 rows. Without `--limit`, it asks for 15.
- `topic` takes a group topic link such as https://www.douban.com/group/topic/<ID>/ and returns the topic text with its replies.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"douban","action":"search","params":{"keyword":"小王子"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `comments`, `reviews`, and `group_topic` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $1.39 |
| `comments` | $1.39 |
| `reviews` | $24.00 |
| `group_topic` | $1.39 |

- Billing is per call, about $0.0014 to $0.024 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- `reviews` is billed by the rows you ask for: each row counts as one call, and rows that do not come back are refunded.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

### Fields

The fields of each capability are documented on the English pages linked below.

- `search`: <https://everyinfra.com/en/douban-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>
- `comments`: <https://everyinfra.com/en/douban-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>
- `reviews`: <https://everyinfra.com/en/douban-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>
- `group_topic`: <https://everyinfra.com/en/douban-api/group_topic?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

### FAQ

**Do I need a Douban account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $1.39 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

**Can I connect the Douban API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>.

**What legal points apply when I use Douban data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Douban data can I get?**

The EveryInfra Douban API has 4 capabilities:

- keyword search
- reviews
- comments
- group topic

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/douban-api?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

### Tested

Before release, we ran the 4 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search 小王子 --out items.csv` | 2026-11-21 09:19 | 5 | $0.001389 |
| `python main.py comments "<item url>" --out comments.csv` | 2026-11-21 09:19 | 20 | $0.001389 |
| `python main.py reviews "<item url>" --limit 3 --out reviews.json` | 2026-11-21 09:20 | 3 | $0.072000 |
| `python main.py topic "<group topic url>" --out topic.json` | 2026-11-21 09:20 | 1 | $0.001389 |

## 中文

本仓库用 Python 或 curl 读豆瓣公开数据：按关键词搜书、电影和音乐条目，读条目的短评和长评，读小组话题和回复。只需一把 EveryInfra API Key，不用豆瓣账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 4 个能力每千次 $1.39 到 $24.00，失败和空结果不收费。豆瓣共 4 个能力：<https://everyinfra.com/douban-api?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/douban-api.git
cd douban-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search 小王子 --out items.csv
python main.py comments "<条目链接>" --out comments.csv
python main.py reviews "<条目链接>" --limit 3 --out reviews.json
python main.py topic "<小组话题链接>" --out topic.json
```

- 条目链接用 `search` 结果里的 `url`，形如 https://book.douban.com/subject/<ID>/；电影和音乐条目也是这种链接。
- `reviews` 按要的条数计费，`--limit 3` 只要 3 条；不加 `--limit` 时默认 15 条。
- `topic` 传小组话题链接，形如 https://www.douban.com/group/topic/<ID>/，返回话题正文和回复。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"douban","action":"search","params":{"keyword":"小王子"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`comments`、`reviews`、`group_topic` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $1.39 |
| 评论 | `comments` | $1.39 |
| 评价 | `reviews` | $24.00 |
| 小组话题 | `group_topic` | $1.39 |

- 按调用次数计费，每次约 $0.0014 到 $0.024；失败、空结果、参数错误和鉴权失败都不收费。
- `reviews` 按要的条数计费，每条算一次调用，没返回的条数退回。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

### 返回字段

下面是这 4 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `title` | 标题。 |
| `subject_type` | 条目类型（电影/书/音乐）。 |
| `year` | 年份。 |
| `author` | 作者。 |
| `cover_url` | 封面。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/douban-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

#### `comments`（评论）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `subject_id` | 条目 ID。 |
| `subject_name` | 条目名称。 |
| `subject_type` | 条目类型（电影/书/音乐）。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `rating` | 评分。 |
| `rating_label` | 评分档位文字。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_url` | 作者在原平台的主页链接。 |
| `author_avatar_url` | 评论者头像。 |
| `vote_count` | 这条评论被点「有用」的次数（comments）。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/douban-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

#### `reviews`（评价）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `subject_id` | 条目 ID。 |
| `subject_name` | 条目名称。 |
| `subject_type` | 条目类型（电影/书/音乐）。 |
| `title` | 标题。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `rating` | 评分。 |
| `rating_label` | 评分档位文字。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_url` | 作者在原平台的主页链接。 |
| `author_avatar_url` | 评论者头像。 |
| `reply_count` | 回复数，通常用于评论的子回复。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/douban-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

#### `group_topic`（小组话题）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `title` | 标题。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `group_id` | 小组 ID。 |
| `group_name` | 小组名。 |
| `group_url` | 小组链接。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_url` | 作者在原平台的主页链接。 |
| `reply_count` | 回复数，通常用于评论的子回复。 |
| `replies` | 回复列表。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/douban-api/group_topic?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

### 常见问题

**调用时要不要提供豆瓣账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $1.39 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

**能把豆瓣接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>。

**用豆瓣数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到豆瓣的哪些数据？**

豆瓣有 4 个能力：关键词搜索、评价、评论、小组话题。每个能力的参数和返回字段见平台页 <https://everyinfra.com/douban-api?utm_source=github&utm_medium=example_repo&utm_campaign=douban-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 4 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search 小王子 --out items.csv` | 2026-11-21 09:19 | 5 | $0.001389 |
| `python main.py comments "<条目链接>" --out comments.csv` | 2026-11-21 09:19 | 20 | $0.001389 |
| `python main.py reviews "<条目链接>" --limit 3 --out reviews.json` | 2026-11-21 09:20 | 3 | $0.072000 |
| `python main.py topic "<小组话题链接>" --out topic.json` | 2026-11-21 09:20 | 1 | $0.001389 |

`reviews` 返回的一条（正文截到 60 字，作者字段和评分字段没放进来）：

```json
{
  "id": "1000104",
  "subject_name": "小王子",
  "subject_type": "book",
  "title": "长大就笨了",
  "text": "那天我第一次打开《小王子》，就呆了。不是因为它的清新剔透，而是圣埃克苏佩里的那些画儿。在过去的一年里，我收到过很多画着小…",
  "reply_count": 445,
  "posted_at": "2005-04-06T03:51:52+00:00"
}
```

## License

MIT
