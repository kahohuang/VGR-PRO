import unittest
from datetime import date, datetime, timedelta

from vgr_ai_assistant import (
    CreatorRecord,
    analyze_records,
    classify_authorization,
    generate_english_message,
    render_dashboard_html,
)


class WorkflowAnalysisTests(unittest.TestCase):
    def test_repeat_creator_does_not_require_resample(self):
        record = CreatorRecord(
            date=datetime(2026, 5, 1),
            username="repeat_creator",
            product="886",
            whatsapp_status="是",
            whatsapp_contact="123456789",
            posted_video_count=2,
            tk_profile_url="https://www.tiktok.com/@repeat_creator",
            cooperation_status="达成合作",
            owner="黄家豪",
            authorization_status=None,
            fathers_day_status=None,
            notes=None,
        )

        [result] = analyze_records([record], today=date(2026, 5, 18))

        self.assertTrue(result["is_repeat_creator"])
        self.assertFalse(result["needs_sample"])
        self.assertEqual(result["stage"], "老达人复合作")
        self.assertEqual(result["next_action"], "确认新视频排期")

    def test_new_creator_waiting_for_sample_application_is_detected(self):
        record = CreatorRecord(
            date=datetime(2026, 5, 10),
            username="new_creator",
            product="886",
            whatsapp_status="是",
            whatsapp_contact="123456789",
            posted_video_count=0,
            tk_profile_url="https://www.tiktok.com/@new_creator",
            cooperation_status="达成合作",
            owner="黄家豪",
            authorization_status=None,
            fathers_day_status=None,
            notes=None,
        )

        [result] = analyze_records([record], today=date(2026, 5, 18))

        self.assertFalse(result["is_repeat_creator"])
        self.assertTrue(result["needs_sample"])
        self.assertEqual(result["stage"], "待申请样品")
        self.assertEqual(result["blocker"], "已同意合作但未申请样品")

    def test_video_posted_without_authorization_requests_ad_code(self):
        record = CreatorRecord(
            date=datetime(2026, 5, 3),
            username="posted_creator",
            product="886",
            whatsapp_status="是",
            whatsapp_contact="123456789",
            posted_video_count=1,
            tk_profile_url="https://www.tiktok.com/@posted_creator",
            cooperation_status="视频已发布",
            owner="黄家豪",
            authorization_status="否",
            fathers_day_status=None,
            notes=None,
        )

        [result] = analyze_records([record], today=date(2026, 5, 18))

        self.assertEqual(result["authorization_type"], "无授权")
        self.assertEqual(result["stage"], "待获取ad code")
        self.assertEqual(result["next_action"], "催ad code")

    def test_account_authorization_is_separate_from_ad_code(self):
        self.assertEqual(classify_authorization("账号已授权"), "账号已授权")
        self.assertEqual(classify_authorization("#abc123xyz"), "ad code")
        self.assertEqual(classify_authorization("是"), "ad code")
        self.assertEqual(classify_authorization("否"), "无授权")

    def test_closed_creator_is_not_marked_high_priority(self):
        record = CreatorRecord(
            date=datetime(2026, 5, 3),
            username="closed_creator",
            product="886",
            whatsapp_status="是",
            whatsapp_contact="123456789",
            posted_video_count=0,
            tk_profile_url="https://www.tiktok.com/@closed_creator",
            cooperation_status="拒绝合作",
            owner="黄家豪",
            authorization_status=None,
            fathers_day_status=None,
            notes=None,
        )

        [result] = analyze_records([record], today=date(2026, 5, 18))

        self.assertEqual(result["stage"], "已关闭")
        self.assertEqual(result["priority"], "低")


class MessageGenerationTests(unittest.TestCase):
    def test_sample_application_message_mentions_review_and_soft_tone(self):
        message = generate_english_message(
            intent_cn="提醒他尽快申请样品，语气轻一点，顺便说我们会尽快审核",
            creator_context={
                "is_repeat_creator": False,
                "has_whatsapp": True,
                "is_fathers_day": False,
                "stage": "待申请样品",
            },
        )

        self.assertIn("sample", message.lower())
        self.assertIn("review", message.lower())
        self.assertIn("whenever you have a moment", message.lower())

    def test_repeat_creator_message_avoids_sample_language(self):
        message = generate_english_message(
            intent_cn="这个是老达人，不用提样品了，问他下周能不能发视频",
            creator_context={
                "is_repeat_creator": True,
                "has_whatsapp": True,
                "is_fathers_day": False,
                "stage": "老达人复合作",
            },
        )

        self.assertIn("next week", message.lower())
        self.assertNotIn("sample", message.lower())

    def test_ad_code_message_stays_polite(self):
        message = generate_english_message(
            intent_cn="他发视频了，帮我催 ad code，别显得太急",
            creator_context={
                "is_repeat_creator": True,
                "has_whatsapp": True,
                "is_fathers_day": False,
                "stage": "待获取ad code",
            },
        )

        self.assertIn("ad code", message.lower())
        self.assertIn("when you get a chance", message.lower())


class DashboardRenderingTests(unittest.TestCase):
    def test_dashboard_html_contains_creator_and_message(self):
        html = render_dashboard_html(
            [
                {
                    "username": "sample_creator",
                    "date": "2026-05-10",
                    "stage": "待申请样品",
                    "priority": "高",
                    "blocker": "已同意合作但未申请样品",
                    "next_action": "提醒申请样品",
                    "is_repeat_creator": False,
                    "needs_sample": True,
                    "has_whatsapp": True,
                    "whatsapp_contact": "+17736366897",
                    "tk_profile_url": "https://www.tiktok.com/@sample_creator",
                    "is_fathers_day": False,
                    "stalled_days": 8,
                    "english_message": "Hey bro, please submit the sample request.",
                    "posted_video_count": 2,
                    "authorization_raw": "#abc123xyz",
                    "authorization_type": "无授权",
                    "fathers_day_status": "",
                }
            ],
            report_date=date(2026, 5, 18),
        )

        self.assertIn("VGR PRO", html)
        self.assertIn("sample_creator", html)
        self.assertIn("2026-05-10", html)
        self.assertIn("日期", html)
        self.assertIn("+17736366897", html)
        self.assertIn("WhatsApp 联系方式", html)
        self.assertIn("TK主页", html)
        self.assertIn("posted_video_count", html)
        self.assertIn("authorization_raw", html)
        self.assertIn('data-edit-field="posted_video_count"', html)
        self.assertIn('data-edit-field="authorization_raw"', html)
        self.assertIn("normalizeTikTokProfile", html)
        self.assertIn("profileUrl(row)", html)
        self.assertIn("https://www.tiktok.com/@", html)
        self.assertIn('placeholder="达人用户名或 @用户名"', html)
        self.assertIn("min-height: 150px", html)
        self.assertIn("background: var(--paper)", html)
        self.assertIn("filterPublished", html)
        self.assertIn("filterCooperated", html)
        self.assertIn("filterReplied", html)
        self.assertIn("#abc123xyz", html)
        self.assertIn("https://www.tiktok.com/@sample_creator", html)
        self.assertIn("copyTikTok", html)
        self.assertIn("copyWhatsapp", html)
        self.assertIn('id="pageSize"', html)
        self.assertIn('value="100" selected', html)
        self.assertIn('data-page-action="prev"', html)
        self.assertIn('data-page-action="next"', html)
        self.assertIn('class="list-head"', html)
        self.assertIn(".list-head", html)
        self.assertIn("position: sticky", html)
        self.assertIn("contact-action-row", html)
        self.assertIn("contact-inline-actions", html)
        self.assertIn('class="action-button"', html)
        self.assertIn("compact-action", html)
        self.assertIn("message-head", html)
        self.assertIn("message-actions", html)
        self.assertIn("editable-grid", html)
        self.assertIn("applyEdit", html)
        self.assertIn("deleteCreator", html)
        self.assertIn("deleteCurrent", html)
        self.assertIn("删除记录", html)
        self.assertIn("确认删除这个达人吗", html)
        self.assertIn("addCreator", html)
        self.assertIn("renderNewCreatorForm", html)
        self.assertIn("newCreator", html)
        self.assertIn("新增达人", html)
        self.assertIn("应用到页面", html)
        self.assertIn('type="date" data-edit-field="date"', html)
        self.assertIn('data-edit-field="whatsapp_contact"', html)
        self.assertIn('<select data-edit-field="stage"', html)
        self.assertIn('<select data-edit-field="next_action"', html)
        self.assertIn("stageOptionsHtml", html)
        self.assertIn("actionOptionsHtml", html)
        self.assertIn("messageEditor", html)
        self.assertIn("confirmMessageEdit", html)
        self.assertIn("hidden-action", html)
        self.assertIn("messageChanged", html)
        self.assertNotIn('data-edit-field="english_message"', html)
        self.assertNotIn("applyLocalEdit", html)
        self.assertNotIn("save-note", html)
        self.assertNotIn('textContent = \'已复制\'', html)
        self.assertNotIn("textContent = '已复制'", html)
        self.assertNotIn("escapeHtml(row.tk_profile_url)</a>", html)
        for page_size in ("50", "100", "200", "300", "500"):
            self.assertIn(f'value="{page_size}"', html)
        self.assertNotIn("WA:", html)
        self.assertIn("Hey bro, please submit the sample request.", html)
        self.assertIn("data-dashboard", html)


if __name__ == "__main__":
    unittest.main()
