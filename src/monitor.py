#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Skills Monitor - 主入口
监控多个技能源，评估兼容性和安全性，生成报告
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from fetchers.github_fetcher import GitHubSkillFetcher
from fetchers.skills_sh_fetcher import SkillsShFetcher
from evaluators.compatibility_checker import OpenCodeCompatibilityChecker
from evaluators.security_scanner import SecurityScanner
from evaluators.value_assessor import ValueAssessor
from reporters.email_reporter import EmailReporter
from reporters.html_generator_enhanced import HTMLReportGenerator
from utils.database import SkillsDatabase
from utils.logger import setup_logger

# 配置日志
logger = setup_logger()

# 监控的技能仓库列表
MONITORED_REPOS = [
    {"owner": "anthropics", "repo": "skills", "name": "Anthropic官方"},
    {"owner": "vercel-labs", "repo": "skills", "name": "Vercel Labs"},
    {"owner": "vercel-labs", "repo": "agent-skills", "name": "Vercel Agent"},
    {"owner": "aiskillstore", "repo": "marketplace", "name": "SkillStore"},
    {"owner": "clawhub", "repo": "skills", "name": "ClawHub"},
    {"owner": "skillhub", "repo": "community", "name": "SkillHub"},
    {"owner": "inferencesh", "repo": "skills", "name": "Inference.sh"},
]

# skills.sh API配置
SKILLS_SH_SOURCES = [
    {"url": "https://skills.sh/api/skills", "name": "skills.sh主站"},
]


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("AI技能监控系统启动")
    logger.info(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    # 初始化数据库
    db = SkillsDatabase("data/skills.db")

    # 收集所有技能
    all_skills = []

    # 1. 从GitHub获取
    logger.info("\n[1/4] 从GitHub获取技能更新...")
    github_token = os.getenv("GH_TOKEN")
    github_fetcher = GitHubSkillFetcher(github_token)  # 支持无token匿名访问

    for repo_info in MONITORED_REPOS:
        try:
            skills = github_fetcher.fetch_recent_skills(
                repo_info["owner"], repo_info["repo"]
            )
            logger.info(f"  ✓ {repo_info['name']}: 获取到 {len(skills)} 个技能")
            all_skills.extend(skills)
        except Exception as e:
            logger.error(f"  ✗ {repo_info['name']}: {str(e)}")

    # 2. 从skills.sh获取
    logger.info("\n[2/4] 从skills.sh获取技能...")
    skills_sh_fetcher = SkillsShFetcher()
    try:
        skills_sh_data = skills_sh_fetcher.fetch_trending(limit=20)
        logger.info(f"  ✓ skills.sh: 获取到 {len(skills_sh_data)} 个热门技能")
        all_skills.extend(skills_sh_data)
    except Exception as e:
        logger.error(f"  ✗ skills.sh: {str(e)}")

    # 3. 数据去重
    logger.info("\n[3/4] 数据清洗与去重...")
    unique_skills = deduplicate_skills(all_skills)
    logger.info(f"  → 去重后: {len(unique_skills)} 个技能")

    # 4. 评估技能
    logger.info("\n[4/4] 评估技能...")
    evaluated_skills = evaluate_skills(unique_skills)

    # 5. 存储到数据库
    logger.info("\n存储到数据库...")
    db.save_skills(evaluated_skills)

    # 6. 生成报告
    logger.info("\n生成报告...")
    report_generator = HTMLReportGenerator()
    html_report = report_generator.generate(evaluated_skills)

    # 保存报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/report_{timestamp}.html"
    latest_path = "reports/latest.html"

    Path(report_path).parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_report)
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(html_report)

    # 保存JSON数据
    json_path = f"reports/data_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(evaluated_skills, f, ensure_ascii=False, indent=2)

    logger.info(f"  ✓ HTML报告: {report_path}")
    logger.info(f"  ✓ JSON数据: {json_path}")

    # 7. 发送邮件(非测试模式)
    test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
    if not test_mode:
        logger.info("\n发送邮件报告...")
        email_reporter = EmailReporter()
        try:
            email_reporter.send_report(evaluated_skills, html_report)
            logger.info("  ✓ 邮件发送成功")
        except Exception as e:
            logger.error(f"  ✗ 邮件发送失败: {str(e)}")
    else:
        logger.info("\n[测试模式] 跳过邮件发送")

    # 输出摘要
    print_summary(evaluated_skills)

    logger.info("\n监控完成!")
    return 0


def deduplicate_skills(skills: list) -> list:
    """按名称和来源去重技能"""
    seen = set()
    unique = []
    for skill in skills:
        key = f"{skill.get('name', '')}_{skill.get('source', '')}"
        if key not in seen:
            seen.add(key)
            unique.append(skill)
    return unique


def evaluate_skills(skills: list) -> list:
    """评估所有技能"""
    compat_checker = OpenCodeCompatibilityChecker()
    security_scanner = SecurityScanner()
    value_assessor = ValueAssessor()

    evaluated = []
    for i, skill in enumerate(skills, 1):
        logger.info(f"  评估 [{i}/{len(skills)}]: {skill.get('name', 'Unknown')}")

        # 兼容性检查
        skill["compatibility"] = compat_checker.check(skill)

        # 安全扫描
        skill["security"] = security_scanner.scan(skill)

        # 价值评估
        skill["value"] = value_assessor.assess(skill)

        # 推荐等级
        skill["recommendation"] = calculate_recommendation(skill)

        evaluated.append(skill)

    return evaluated


def calculate_recommendation(skill: dict) -> dict:
    """计算推荐等级"""
    compat = skill.get("compatibility", {})
    security = skill.get("security", {})
    value = skill.get("value", {})

    # 安全红线
    if security.get("risk_level") == "HIGH":
        return {"level": "不推荐", "reason": "存在严重安全风险", "priority": 0}

    # 兼容性判断
    compat_level = compat.get("level", "")
    if compat_level == "完全兼容":
        level = "必装" if value.get("score", 0) > 7 else "可选"
    elif compat_level == "部分兼容":
        level = "可选"
    else:
        level = "不推荐"

    return {
        "level": level,
        "reason": f"兼容性:{compat_level}, 安全:{security.get('risk_level', '未知')}",
        "priority": 3 if level == "必装" else (2 if level == "可选" else 1),
    }


def print_summary(skills: list):
    """打印监控摘要"""
    total = len(skills)
    must_install = sum(
        1 for s in skills if s.get("recommendation", {}).get("level") == "必装"
    )
    optional = sum(
        1 for s in skills if s.get("recommendation", {}).get("level") == "可选"
    )
    not_recommended = sum(
        1 for s in skills if s.get("recommendation", {}).get("level") == "不推荐"
    )
    fully_compat = sum(
        1 for s in skills if s.get("compatibility", {}).get("level") == "完全兼容"
    )
    high_risk = sum(
        1 for s in skills if s.get("security", {}).get("risk_level") == "HIGH"
    )

    logger.info("\n" + "=" * 60)
    logger.info("监控摘要")
    logger.info("=" * 60)
    logger.info(f"总技能数:    {total}")
    logger.info(f"完全兼容:    {fully_compat}")
    logger.info(f"必装推荐:    {must_install}")
    logger.info(f"可选安装:    {optional}")
    logger.info(f"不推荐:      {not_recommended}")
    logger.info(f"高风险警告:  {high_risk}")
    logger.info("=" * 60)

    # 控制台输出
    print("\n" + "=" * 60)
    print("🤖 AI技能监控日报")
    print("=" * 60)
    print(f"监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"新增技能: {total} 个")
    print(f"必装推荐: {must_install} 个")
    print(f"高风险:   {high_risk} 个")
    print("=" * 60)


if __name__ == "__main__":
    sys.exit(main())
