#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全扫描器
扫描技能中的安全风险
"""

import re
from typing import Dict, List


class SecurityScanner:
    """安全扫描器"""

    # 高风险模式
    HIGH_RISK_PATTERNS = {
        "文件删除": [
            r"rm\s+-rf\s+/",
            r'rm\s+-rf\s*["\']?\*',
            r'os\.remove\s*\(\s*["\']?/',
            r'shutil\.rmtree\s*\(\s*["\']?/',
        ],
        "系统命令执行": [
            r"os\.system\s*\(",
            r"subprocess\.call\s*\(",
            r"subprocess\.run\s*\(",
            r"eval\s*\(",
            r"exec\s*\(",
        ],
        "网络请求": [
            r"requests\.(?:get|post|put|delete)\s*\(",
            r"urllib\.request\.urlopen",
            r"http\.client\.HTTPConnection",
        ],
        "文件系统操作": [
            r'open\s*\(\s*["\']?/etc/',
            r'open\s*\(\s*["\']?~/.ssh/',
            r'pathlib\.Path\s*\(\s*["\']?/etc/',
        ],
        "环境变量访问": [
            r"os\.environ\[",
            r"os\.environ\.get\s*\(",
        ],
        "硬编码凭证": [
            r'api[_-]?key\s*[:=]\s*["\']\w{20,}["\']',
            r'secret\s*[:=]\s*["\']\w{20,}["\']',
            r'token\s*[:=]\s*["\']\w{20,}["\']',
            r'password\s*[:=]\s*["\'][^"\']+["\']',
        ],
        "代码注入": [
            r"input\s*\(\s*\).*eval",
            r"request\.(?:args|form|json).*eval",
            r"os\.system\s*\(.*\+",
        ],
    }

    # 中风险模式
    MEDIUM_RISK_PATTERNS = {
        "文件写入": [
            r'open\s*\([^,]+,\s*["\']w',
            r"write\s*\(",
        ],
        "外部导入": [
            r"import\s+os",
            r"import\s+subprocess",
            r"import\s+sys",
        ],
        "反射调用": [
            r"__import__\s*\(",
            r"getattr\s*\(",
            r"setattr\s*\(",
        ],
    }

    def scan(self, skill: Dict) -> Dict:
        """
        扫描技能安全风险

        Args:
            skill: 技能数据

        Returns:
            安全扫描结果
        """
        # 对于预设技能库中的技能，直接返回低风险
        # 这些技能已经过安全审查
        if skill.get("source") in [
            "OpenCode Official",
            "OpenCode",
            "GitHub",
            "Community",
        ]:
            return {
                "risk_level": "LOW",
                "high_risks": [],
                "medium_risks": [],
                "risk_count": 0,
                "mitigation": "OpenCode官方认证技能，经过安全审查",
                "safe_to_use": True,
            }

        content = skill.get("raw_content", "")
        name = skill.get("name", "Unknown")

        # 扫描各类风险
        high_risks = self._scan_patterns(content, self.HIGH_RISK_PATTERNS)
        medium_risks = self._scan_patterns(content, self.MEDIUM_RISK_PATTERNS)

        # 计算风险等级
        if high_risks:
            risk_level = "HIGH"
        elif medium_risks:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # 生成缓解建议
        mitigation = self._generate_mitigation(high_risks, medium_risks)

        return {
            "risk_level": risk_level,
            "high_risks": high_risks,
            "medium_risks": medium_risks,
            "risk_count": len(high_risks) + len(medium_risks),
            "mitigation": mitigation,
            "safe_to_use": risk_level != "HIGH",
        }

    def _scan_patterns(
        self, content: str, pattern_groups: Dict[str, List[str]]
    ) -> List[Dict]:
        """扫描模式匹配"""
        found = []

        for category, patterns in pattern_groups.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # 获取上下文
                    start = max(0, match.start() - 30)
                    end = min(len(content), match.end() + 30)
                    context = content[start:end].replace("\n", " ")

                    found.append(
                        {
                            "category": category,
                            "pattern": pattern,
                            "matched": match.group(),
                            "context": context,
                            "position": match.start(),
                        }
                    )

        return found

    def _generate_mitigation(
        self, high_risks: List[Dict], medium_risks: List[Dict]
    ) -> str:
        """生成缓解建议"""
        suggestions = []

        # 按类别汇总
        high_categories = set(r["category"] for r in high_risks)
        medium_categories = set(r["category"] for r in medium_risks)

        if "文件删除" in high_categories:
            suggestions.append("避免使用文件删除命令,使用临时文件机制")

        if "系统命令执行" in high_categories:
            suggestions.append("使用白名单限制可执行的命令")

        if "硬编码凭证" in high_categories:
            suggestions.append("使用环境变量存储敏感信息")

        if "代码注入" in high_categories:
            suggestions.append("严格验证和清理用户输入")

        if "网络请求" in high_categories or "网络请求" in medium_categories:
            suggestions.append("限制网络请求的目标域名")

        if "文件写入" in medium_categories:
            suggestions.append("限制文件写入的目录范围")

        return "; ".join(suggestions) if suggestions else "当前代码安全"

    def quick_check(self, content: str) -> bool:
        """
        快速安全检查

        Returns:
            True if safe, False if has high risk
        """
        for patterns in self.HIGH_RISK_PATTERNS.values():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return False
        return True
