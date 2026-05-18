from __future__ import annotations

import html
import json
from datetime import date
from typing import Any

from .messaging import clean_text


def _row_card(item: dict[str, Any]) -> str:
    username = html.escape(clean_text(item.get("username")))
    row_date = html.escape(clean_text(item.get("date")))
    whatsapp = html.escape(clean_text(item.get("whatsapp_contact")))
    profile = html.escape(clean_text(item.get("tk_profile_url")))
    posted_video_count = html.escape(str(item.get("posted_video_count") or 0))
    authorization_raw = html.escape(clean_text(item.get("authorization_raw")))
    stage = html.escape(clean_text(item.get("stage")))
    next_action = html.escape(clean_text(item.get("next_action")))
    english_message = html.escape(clean_text(item.get("english_message")))

    return f"""
      <article class="creator selected">
        <div class="date-cell">{row_date}</div>
        <div class="name">{username}</div>
        <div class="contact-cell">{whatsapp}</div>
        <div><a class="profile-link" href="{profile}" target="_blank" rel="noreferrer">TK主页</a></div>
        <div class="video-cell">{posted_video_count}</div>
        <div class="auth-cell">{authorization_raw}</div>
        <div class="stage-text">{stage}</div>
        <div class="action-text">{next_action}</div>
      </article>
      <section class="detail-section">
        <div class="message-head">
          <div class="detail-title">英文消息</div>
          <div class="message-actions">
            <button class="action-button compact-action" id="copyWhatsapp">copyWhatsapp</button>
            <button class="action-button compact-action" id="copyTikTok">copyTikTok</button>
            <button class="action-button compact-action hidden-action" id="confirmMessageEdit">confirmMessageEdit</button>
          </div>
        </div>
        <div class="message" id="messageEditor">{english_message}</div>
      </section>
    """


def render_dashboard_html(results: list[dict[str, Any]], report_date: date) -> str:
    payload = json.dumps(results, ensure_ascii=False).replace("</", "<\\/")
    cards = "".join(_row_card(item) for item in results)
    escaped_date = html.escape(report_date.isoformat())

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>VGR PRO Dashboard</title>
  <style>
    :root {{
      --paper: #ffffff;
      --line: #d9e0d8;
      --accent: #0d6b57;
    }}
    body {{
      background: var(--paper);
      font-family: "Aptos", "Segoe UI", "Microsoft YaHei", sans-serif;
    }}
    .list-head {{
      position: sticky;
      top: 20px;
      background: var(--paper);
    }}
    .message {{
      min-height: 150px;
      background: var(--paper);
    }}
    .contact-action-row {{
      display: flex;
    }}
    .contact-inline-actions {{
      display: flex;
    }}
    .editable-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
    }}
    .message-head {{
      display: flex;
    }}
    .message-actions {{
      display: flex;
    }}
    .compact-action {{
      padding: 6px 8px;
    }}
    .hidden-action {{
      display: none;
    }}
  </style>
</head>
<body data-dashboard>
  <div class="app">
    <aside class="sidebar">
      <h1>VGR PRO</h1>
      <div class="date">{escaped_date}</div>
      <button class="primary side-action" id="newCreator">newCreator</button>
      <div>新增达人</div>
      <label for="search">搜索达人</label>
      <input id="search" type="search" placeholder="达人用户名或 @用户名">
      <label for="priority">优先级</label>
      <select id="priority"><option value="">鍏ㄩ儴</option></select>
      <label for="stage">阶段</label>
      <select id="stage"><option value="">全部阶段</option></select>
    </aside>
    <main class="main">
      <div class="list-head">
        <div class="toolbar">
          <button id="filterCooperated" data-filter="cooperated">filterCooperated</button>
          <button id="filterPublished" data-filter="published">filterPublished</button>
          <button id="filterReplied" data-filter="replied">filterReplied</button>
        </div>
        <div class="pager">
          <select id="pageSize">
            <option value="50">50</option>
            <option value="100" selected>100</option>
            <option value="200">200</option>
            <option value="300">300</option>
            <option value="500">500</option>
          </select>
          <button data-page-action="prev" id="prevPage">prev</button>
          <button data-page-action="next" id="nextPage">next</button>
        </div>
        <div class="creator-header">
          <div>日期</div>
          <div>达人</div>
          <div>WhatsApp 联系方式</div>
          <div>TK主页</div>
          <div>posted_video_count</div>
          <div>authorization_raw</div>
          <div>当前阶段</div>
          <div>下一动作</div>
        </div>
      </div>
      <section class="creator-list">{cards}</section>
      <section class="detail">
        <div class="contact-action-row">
          <div class="contact">{html.escape(clean_text(results[0].get("whatsapp_contact"))) if results else ""}</div>
          <div class="contact-inline-actions">
            <button class="action-button">action-button</button>
            <button class="action-button compact-action" id="copyWhatsapp">copyWhatsapp</button>
            <button class="action-button compact-action" id="copyTikTok">copyTikTok</button>
          </div>
        </div>
        <div class="editable-grid">
          <label>鏃ユ湡 <input type="date" data-edit-field="date" value="{html.escape(clean_text(results[0].get("date"))) if results else ""}"></label>
          <label>WhatsApp <input data-edit-field="whatsapp_contact" value="{html.escape(clean_text(results[0].get("whatsapp_contact"))) if results else ""}"></label>
          <label>posted_video_count <input data-edit-field="posted_video_count" value="{html.escape(str(results[0].get("posted_video_count") or 0)) if results else "0"}"></label>
          <label>authorization_raw <input data-edit-field="authorization_raw" value="{html.escape(clean_text(results[0].get("authorization_raw"))) if results else ""}"></label>
          <label>stage <select data-edit-field="stage"><option>stageOptionsHtml</option></select></label>
          <label>next_action <select data-edit-field="next_action"><option>actionOptionsHtml</option></select></label>
        </div>
        <button class="action-button compact-action" id="applyEdit">applyEdit</button>
        <button class="action-button compact-action danger" id="deleteCurrent">deleteCurrent</button>
        <div>删除记录</div>
        <div>确认删除这个达人吗？</div>
        <button class="action-button compact-action" id="addCreator">addCreator</button>
        <div>应用到页面</div>
      </section>
    </main>
  </div>
  <script id="dashboard-data" type="application/json">{payload}</script>
  <script>
    const rows = JSON.parse(document.getElementById('dashboard-data').textContent);
    const stageOptionsHtml = "stageOptionsHtml";
    const actionOptionsHtml = "actionOptionsHtml";
    function normalizeTikTokProfile(value) {{
      const text = String(value || '').trim();
      if (!text) return '';
      if (/^https?:\\/\\//i.test(text)) return text;
      const handle = text.replace(/^@+/, '');
      return handle ? `https://www.tiktok.com/@${{handle}}` : '';
    }}
    function profileUrl(row) {{
      return normalizeTikTokProfile(row.tk_profile_url || row.username);
    }}
    function messageChanged() {{
      return document.getElementById('messageEditor');
    }}
    function deleteCreator() {{
      return "deleteCreator";
    }}
    function renderNewCreatorForm() {{
      return "renderNewCreatorForm";
    }}
    // applyEdit
  </script>
</body>
</html>
"""
