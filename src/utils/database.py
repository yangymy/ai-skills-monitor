#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能数据库
使用SQLite存储技能数据
"""

import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class SkillsDatabase:
    """技能数据库"""

    def __init__(self, db_path: str = "data/skills.db"):
        """
        初始化数据库

        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建技能表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                source TEXT NOT NULL,
                author TEXT,
                version TEXT,
                description TEXT,
                url TEXT,
                tags TEXT,
                raw_content TEXT,
                compatibility_level TEXT,
                compatibility_score REAL,
                security_level TEXT,
                security_risks TEXT,
                value_score REAL,
                value_tags TEXT,
                recommendation_level TEXT,
                recommendation_reason TEXT,
                install_count INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT,
                first_seen TEXT,
                last_checked TEXT
            )
        """)

        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_name ON skills(name)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_source ON skills(source)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_date ON skills(last_checked)
        """)

        conn.commit()
        conn.close()

    def save_skills(self, skills: List[Dict]):
        """
        保存技能列表

        Args:
            skills: 技能列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().isoformat()

        for skill in skills:
            # 检查是否已存在
            cursor.execute(
                "SELECT id, first_seen FROM skills WHERE name = ? AND source = ?",
                (skill.get("name"), skill.get("source")),
            )
            existing = cursor.fetchone()

            # 提取评估数据
            compat = skill.get("compatibility", {})
            security = skill.get("security", {})
            value = skill.get("value", {})
            recommendation = skill.get("recommendation", {})

            if existing:
                # 更新现有记录
                cursor.execute(
                    """
                    UPDATE skills SET
                        description = ?,
                        version = ?,
                        url = ?,
                        tags = ?,
                        raw_content = ?,
                        compatibility_level = ?,
                        compatibility_score = ?,
                        security_level = ?,
                        security_risks = ?,
                        value_score = ?,
                        value_tags = ?,
                        recommendation_level = ?,
                        recommendation_reason = ?,
                        install_count = ?,
                        updated_at = ?,
                        last_checked = ?
                    WHERE id = ?
                """,
                    (
                        skill.get("description", ""),
                        skill.get("version", "1.0.0"),
                        skill.get("url", ""),
                        json.dumps(skill.get("tags", [])),
                        skill.get("raw_content", "")[:5000],
                        compat.get("level", ""),
                        compat.get("score", 0),
                        security.get("risk_level", ""),
                        json.dumps(security.get("high_risks", [])),
                        value.get("score", 0),
                        json.dumps(value.get("tags", [])),
                        recommendation.get("level", ""),
                        recommendation.get("reason", ""),
                        skill.get("install_count", 0),
                        skill.get("updated_at", now),
                        now,
                        existing[0],
                    ),
                )
            else:
                # 插入新记录
                cursor.execute(
                    """
                    INSERT INTO skills (
                        name, source, author, version, description, url, tags,
                        raw_content, compatibility_level, compatibility_score,
                        security_level, security_risks, value_score, value_tags,
                        recommendation_level, recommendation_reason, install_count,
                        created_at, updated_at, first_seen, last_checked
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        skill.get("name", ""),
                        skill.get("source", ""),
                        skill.get("author", ""),
                        skill.get("version", "1.0.0"),
                        skill.get("description", ""),
                        skill.get("url", ""),
                        json.dumps(skill.get("tags", [])),
                        skill.get("raw_content", "")[:5000],
                        compat.get("level", ""),
                        compat.get("score", 0),
                        security.get("risk_level", ""),
                        json.dumps(security.get("high_risks", [])),
                        value.get("score", 0),
                        json.dumps(value.get("tags", [])),
                        recommendation.get("level", ""),
                        recommendation.get("reason", ""),
                        skill.get("install_count", 0),
                        skill.get("updated_at", now),
                        skill.get("updated_at", now),
                        now,
                        now,
                    ),
                )

        conn.commit()
        conn.close()

    def get_recent_skills(self, days: int = 7) -> List[Dict]:
        """
        获取最近添加的技能

        Args:
            days: 天数

        Returns:
            技能列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM skills 
            WHERE first_seen >= datetime('now', '-{} days')
            ORDER BY first_seen DESC
        """.format(days)
        )

        rows = cursor.fetchall()
        conn.close()

        return self._rows_to_dicts(rows)

    def get_skills_by_recommendation(self, level: str) -> List[Dict]:
        """
        按推荐等级获取技能

        Args:
            level: 推荐等级(必装/可选/不推荐)

        Returns:
            技能列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM skills WHERE recommendation_level = ? ORDER BY value_score DESC",
            (level,),
        )

        rows = cursor.fetchall()
        conn.close()

        return self._rows_to_dicts(rows)

    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # 总数
        cursor.execute("SELECT COUNT(*) FROM skills")
        stats["total"] = cursor.fetchone()[0]

        # 按推荐等级统计
        cursor.execute("""
            SELECT recommendation_level, COUNT(*) 
            FROM skills 
            GROUP BY recommendation_level
        """)
        stats["by_recommendation"] = dict(cursor.fetchall())

        # 按安全风险统计
        cursor.execute("""
            SELECT security_level, COUNT(*) 
            FROM skills 
            GROUP BY security_level
        """)
        stats["by_security"] = dict(cursor.fetchall())

        # 今日新增
        cursor.execute("""
            SELECT COUNT(*) FROM skills 
            WHERE first_seen >= date('now')
        """)
        stats["today_new"] = cursor.fetchone()[0]

        conn.close()

        return stats

    def _rows_to_dicts(self, rows) -> List[Dict]:
        """将数据库行转换为字典"""
        columns = [
            "id",
            "name",
            "source",
            "author",
            "version",
            "description",
            "url",
            "tags",
            "raw_content",
            "compatibility_level",
            "compatibility_score",
            "security_level",
            "security_risks",
            "value_score",
            "value_tags",
            "recommendation_level",
            "recommendation_reason",
            "install_count",
            "created_at",
            "updated_at",
            "first_seen",
            "last_checked",
        ]

        results = []
        for row in rows:
            skill = dict(zip(columns, row))
            # 解析JSON字段
            for field in ["tags", "security_risks", "value_tags"]:
                try:
                    skill[field] = json.loads(skill.get(field, "[]"))
                except:
                    skill[field] = []
            results.append(skill)

        return results
