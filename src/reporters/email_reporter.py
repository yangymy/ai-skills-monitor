#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件报告发送器
通过邮件发送监控报告
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional


class EmailReporter:
    """邮件报告发送器"""

    def __init__(self):
        """初始化邮件配置"""
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.recipient = os.getenv("EMAIL_RECIPIENT", "")

        # SendGrid配置(优先使用)
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")

    def send_report(self, skills: List[Dict], html_content: str) -> bool:
        """
        发送报告邮件

        Args:
            skills: 技能列表
            html_content: HTML报告内容

        Returns:
            发送成功返回True
        """
        if self.sendgrid_api_key:
            return self._send_via_sendgrid(skills, html_content)
        else:
            return self._send_via_smtp(skills, html_content)

    def _send_via_sendgrid(self, skills: List[Dict], html_content: str) -> bool:
        """通过SendGrid发送"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail

            # 生成摘要
            summary = self._generate_summary(skills)

            message = Mail(
                from_email=self.smtp_user or "ai-skills-monitor@noreply.com",
                to_emails=self.recipient,
                subject=f"🤖 AI技能监控日报 - {summary}",
                html_content=html_content,
            )

            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)

            return response.status_code in [200, 201, 202]

        except Exception as e:
            print(f"SendGrid发送失败: {e}")
            return False

    def _send_via_smtp(self, skills: List[Dict], html_content: str) -> bool:
        """通过SMTP发送"""
        if not all([self.smtp_user, self.smtp_password, self.recipient]):
            print("SMTP配置不完整,跳过邮件发送")
            return False

        try:
            # 生成摘要
            summary = self._generate_summary(skills)

            # 创建邮件
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"🤖 AI技能监控日报 - {summary}"
            msg["From"] = self.smtp_user
            msg["To"] = self.recipient

            # 添加HTML内容
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            # 连接SMTP服务器
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)

            # 发送邮件
            server.sendmail(self.smtp_user, self.recipient, msg.as_string())
            server.quit()

            return True

        except Exception as e:
            print(f"SMTP发送失败: {e}")
            return False

    def _generate_summary(self, skills: List[Dict]) -> str:
        """生成邮件主题摘要"""
        total = len(skills)
        must_install = sum(
            1 for s in skills if s.get("recommendation", {}).get("level") == "必装"
        )
        high_risk = sum(
            1 for s in skills if s.get("security", {}).get("risk_level") == "HIGH"
        )

        summary = f"共{total}个技能"
        if must_install > 0:
            summary += f", {must_install}个必装"
        if high_risk > 0:
            summary += f", {high_risk}个高风险"

        return summary

    def test_connection(self) -> bool:
        """测试邮件连接"""
        try:
            if self.sendgrid_api_key:
                from sendgrid import SendGridAPIClient

                sg = SendGridAPIClient(self.sendgrid_api_key)
                # 尝试获取账户信息
                response = sg.client.user.profile.get()
                return response.status_code == 200
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.quit()
                return True
        except Exception as e:
            print(f"邮件连接测试失败: {e}")
            return False
