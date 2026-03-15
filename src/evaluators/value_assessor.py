#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价值评估器
评估技能的使用价值和质量
"""

import re
from typing import Dict, List
from datetime import datetime


class ValueAssessor:
    """价值评估器"""

    def assess(self, skill: Dict) -> Dict:
        """
        评估技能价值

        Args:
            skill: 技能数据

        Returns:
            价值评估结果
        """
        content = skill.get("raw_content", "")

        # 各项指标评分
        scores = {
            "completeness": self._score_completeness(skill, content),
            "documentation": self._score_documentation(content),
            "examples": self._score_examples(content),
            "uniqueness": self._score_uniqueness(skill),
            "maintainability": self._score_maintainability(content),
        }

        # 计算总分
        total_score = sum(scores.values()) / len(scores)

        # 价值标签
        tags = self._generate_value_tags(skill, scores)

        return {
            "score": round(total_score, 1),
            "max_score": 10,
            "breakdown": scores,
            "tags": tags,
            "summary": self._generate_summary(total_score, tags),
        }

    def _score_completeness(self, skill: Dict, content: str) -> float:
        """评估完整性(0-10)"""
        score = 5.0  # 基础分

        # 检查必要字段
        required_fields = ["name", "description", "source"]
        has_fields = sum(1 for f in required_fields if skill.get(f))
        score += (has_fields / len(required_fields)) * 2

        # 检查内容长度
        if len(content) > 1000:
            score += 1.5
        elif len(content) > 500:
            score += 1

        # 检查是否有元数据
        if "---" in content[:200]:
            score += 1.5

        return min(score, 10)

    def _score_documentation(self, content: str) -> float:
        """评估文档质量(0-10)"""
        score = 5.0

        # 标题层级
        if re.search(r"^#{1,2}\s+", content, re.MULTILINE):
            score += 1

        # 分节清晰
        sections = len(re.findall(r"^#{2,3}\s+", content, re.MULTILINE))
        if sections >= 3:
            score += 2
        elif sections >= 1:
            score += 1

        # 描述详细程度
        desc_match = re.search(
            r"(?:描述|Description)[\s\S]{100,500}", content, re.IGNORECASE
        )
        if desc_match:
            score += 1.5

        # 有使用说明
        if re.search(r"(?:使用|Usage|How to)", content, re.IGNORECASE):
            score += 0.5

        return min(score, 10)

    def _score_examples(self, content: str) -> float:
        """评估示例质量(0-10)"""
        score = 3.0

        # 代码块数量
        code_blocks = len(re.findall(r"```[\s\S]*?```", content))
        if code_blocks >= 3:
            score += 4
        elif code_blocks >= 1:
            score += 2

        # 内联代码
        inline_codes = len(re.findall(r"`[^`]+`", content))
        if inline_codes >= 5:
            score += 1.5
        elif inline_codes >= 2:
            score += 0.5

        # 使用示例说明
        if re.search(r"(?:示例|Example|示范)", content, re.IGNORECASE):
            score += 1.5

        return min(score, 10)

    def _score_uniqueness(self, skill: Dict) -> float:
        """评估独特性(0-10)"""
        score = 5.0

        # 特殊标签
        special_tags = ["advanced", "expert", "production", "enterprise"]
        tags = [t.lower() for t in skill.get("tags", [])]
        special_count = sum(1 for t in special_tags if any(t in tag for tag in tags))
        score += special_count * 1.5

        # 安装量
        installs = skill.get("install_count", 0)
        if installs > 1000:
            score += 2
        elif installs > 100:
            score += 1

        # 来源声誉
        source = skill.get("source", "")
        if "anthropic" in source.lower() or "vercel" in source.lower():
            score += 2

        return min(score, 10)

    def _score_maintainability(self, content: str) -> float:
        """评估可维护性(0-10)"""
        score = 5.0

        # 代码复杂度
        complex_patterns = [
            r"for\s+.*for\s+",  # 嵌套循环
            r"if.*if.*if",  # 多层if
            r"lambda.*lambda",  # 嵌套lambda
        ]
        complexity = sum(1 for p in complex_patterns if re.search(p, content))
        score -= complexity * 0.5

        # 注释比例
        comments = len(re.findall(r"#.*$", content, re.MULTILINE))
        lines = len(content.split("\n"))
        comment_ratio = comments / max(lines, 1)
        if comment_ratio > 0.1:
            score += 2
        elif comment_ratio > 0.05:
            score += 1

        # 错误处理
        if re.search(r"try:|except:|finally:", content):
            score += 1.5

        return min(max(score, 0), 10)

    def _generate_value_tags(self, skill: Dict, scores: Dict) -> List[str]:
        """生成价值标签"""
        tags = []

        if scores["completeness"] >= 8:
            tags.append("文档完整")

        if scores["documentation"] >= 8:
            tags.append("说明详细")

        if scores["examples"] >= 8:
            tags.append("示例丰富")

        if scores["uniqueness"] >= 8:
            tags.append("独特功能")

        if scores["maintainability"] >= 8:
            tags.append("易于维护")

        # 基于安装量
        installs = skill.get("install_count", 0)
        if installs > 10000:
            tags.append("社区热门")
        elif installs > 1000:
            tags.append("广泛使用的")

        # 基于来源
        source = skill.get("source", "")
        if "anthropic" in source.lower():
            tags.append("官方推荐")
        elif "vercel" in source.lower():
            tags.append("Vercel认证")

        return tags[:5]  # 最多5个标签

    def _generate_summary(self, score: float, tags: List[str]) -> str:
        """生成价值摘要"""
        if score >= 8:
            return f"高质量技能,强烈推荐。{' '.join(tags[:3])}"
        elif score >= 6:
            return f"良好技能,值得使用。{' '.join(tags[:2])}"
        elif score >= 4:
            return "基础技能,功能可用"
        else:
            return "技能较简单,谨慎评估"
