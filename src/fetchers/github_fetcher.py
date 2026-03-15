#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub技能获取器
从GitHub仓库获取技能更新
"""

import os
import re
import base64
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urlparse


class GitHubSkillFetcher:
    """GitHub技能获取器"""

    def __init__(self, token: Optional[str] = None):
        """
        初始化

        Args:
            token: GitHub Personal Access Token
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-Skills-Monitor/1.0",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

        self.base_url = "https://api.github.com"

    def fetch_recent_skills(self, owner: str, repo: str, hours: int = 24) -> List[Dict]:
        """
        获取技能列表（不限制时间，扫描所有SKILL.md文件）

        Args:
            owner: 仓库所有者
            repo: 仓库名
            hours: 时间窗口(小时) - 已废弃，保留参数兼容

        Returns:
            技能列表
        """
        skills = []

        # 直接扫描仓库中的所有SKILL.md文件
        logger.info(f"  扫描 {owner}/{repo} 中的技能文件...")
        repo_skills = self._scan_repo_skills(owner, repo)
        skills.extend(repo_skills)

        # 尝试获取最近提交（补充更新信息）
        try:
            since = (datetime.now() - timedelta(days=7)).isoformat()
            commits = self._get_commits(owner, repo, since)
            for commit in commits:
                skill_changes = self._extract_skill_changes(owner, repo, commit)
                skills.extend(skill_changes)
        except Exception as e:
            logger.warning(f"  获取commits失败: {e}")

        return skills

    def _get_commits(self, owner: str, repo: str, since: str) -> List[Dict]:
        """获取最近提交"""
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {"since": since, "per_page": 100}

        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"获取commits失败: {e}")
            return []

    def _get_releases(self, owner: str, repo: str, since: str) -> List[Dict]:
        """获取最近发布"""
        url = f"{self.base_url}/repos/{owner}/{repo}/releases"

        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            releases = resp.json()

            # 过滤最近发布
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            recent = [
                r
                for r in releases
                if datetime.fromisoformat(r["published_at"].replace("Z", "+00:00"))
                >= since_dt
            ]
            return recent
        except Exception as e:
            print(f"获取releases失败: {e}")
            return []

    def _extract_skill_changes(self, owner: str, repo: str, commit: Dict) -> List[Dict]:
        """从提交中提取技能变更"""
        skills = []
        commit_sha = commit.get("sha", "")

        # 获取提交详情
        url = f"{self.base_url}/repos/{owner}/{repo}/commits/{commit_sha}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            detail = resp.json()

            # 检查文件变更
            for file in detail.get("files", []):
                filename = file.get("filename", "")
                if "SKILL.md" in filename or filename.endswith(".md"):
                    skill = self._parse_skill_file(owner, repo, filename, commit)
                    if skill:
                        skill["update_type"] = file.get("status", "modified")
                        skill["commit_message"] = commit.get("commit", {}).get(
                            "message", ""
                        )
                        skills.append(skill)
        except Exception as e:
            print(f"提取技能变更失败: {e}")

        return skills

    def _extract_release_skills(
        self, owner: str, repo: str, release: Dict
    ) -> List[Dict]:
        """从发布中提取技能"""
        skills = []

        skill = {
            "name": release.get("name", ""),
            "version": release.get("tag_name", ""),
            "description": release.get("body", "")[:500],
            "author": release.get("author", {}).get("login", ""),
            "updated_at": release.get("published_at"),
            "source": f"github:{owner}/{repo}",
            "url": release.get("html_url", ""),
            "update_type": "release",
        }

        skills.append(skill)
        return skills

    def _scan_repo_skills(self, owner: str, repo: str) -> List[Dict]:
        """扫描仓库中的技能文件"""
        skills = []

        # 常见技能目录
        skill_dirs = ["skills", "skill", ".claude/skills", ".agents/skills"]

        for dir_path in skill_dirs:
            try:
                url = f"{self.base_url}/repos/{owner}/{repo}/contents/{dir_path}"
                resp = requests.get(url, headers=self.headers, timeout=30)

                if resp.status_code != 200:
                    continue

                contents = resp.json()
                if not isinstance(contents, list):
                    continue

                for item in contents:
                    if item.get("type") == "file" and item.get("name", "").endswith(
                        ".md"
                    ):
                        skill = self._parse_skill_from_content(
                            owner, repo, item.get("name", ""), item.get("html_url", "")
                        )
                        if skill:
                            skills.append(skill)

                    # 递归扫描子目录
                    elif item.get("type") == "dir":
                        sub_skills = self._scan_directory(
                            owner, repo, item.get("path", "")
                        )
                        skills.extend(sub_skills)

            except Exception as e:
                continue

        return skills

    def _scan_directory(self, owner: str, repo: str, path: str) -> List[Dict]:
        """扫描目录"""
        skills = []

        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
            resp = requests.get(url, headers=self.headers, timeout=30)

            if resp.status_code != 200:
                return skills

            contents = resp.json()
            if not isinstance(contents, list):
                return skills

            for item in contents:
                if item.get("type") == "file" and item.get("name", "").endswith(".md"):
                    skill = self._parse_skill_from_content(
                        owner, repo, item.get("name", ""), item.get("html_url", "")
                    )
                    if skill:
                        skill["category"] = path.split("/")[-1]
                        skills.append(skill)
        except Exception:
            pass

        return skills

    def _parse_skill_file(
        self, owner: str, repo: str, path: str, commit: Dict
    ) -> Optional[Dict]:
        """解析技能文件"""
        try:
            # 获取文件内容
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
            params = {"ref": commit.get("sha", "")}

            resp = requests.get(url, headers=self.headers, params=params, timeout=30)
            if resp.status_code != 200:
                return None

            data = resp.json()
            content = base64.b64decode(data.get("content", "")).decode("utf-8")

            return self._parse_skill_content(
                owner, repo, path, content, data.get("html_url", "")
            )
        except Exception as e:
            print(f"解析技能文件失败 {path}: {e}")
            return None

    def _parse_skill_from_content(
        self, owner: str, repo: str, name: str, url: str
    ) -> Optional[Dict]:
        """从URL解析技能"""
        try:
            # 转换到raw URL
            raw_url = url.replace("github.com", "raw.githubusercontent.com").replace(
                "/blob/", "/"
            )
            resp = requests.get(raw_url, headers=self.headers, timeout=30)

            if resp.status_code != 200:
                return None

            return self._parse_skill_content(owner, repo, name, resp.text, url)
        except Exception:
            return None

    def _parse_skill_content(
        self, owner: str, repo: str, path: str, content: str, url: str
    ) -> Dict:
        """解析技能内容"""
        # 提取技能名称(去掉.md后缀)
        name = path.replace(".md", "").replace("SKILL", "").strip("-_/")

        # 解析元数据
        metadata = self._extract_metadata(content)

        # 提取描述(前200字符)
        description = self._extract_description(content)

        skill = {
            "name": metadata.get("name") or name,
            "description": description,
            "author": metadata.get("author") or f"{owner}/{repo}",
            "version": metadata.get("version") or "1.0.0",
            "tags": metadata.get("tags", []),
            "updated_at": datetime.now().isoformat(),
            "source": f"github:{owner}/{repo}",
            "url": url,
            "raw_content": content[:5000],  # 限制内容大小
            "path": path,
        }

        return skill

    def _extract_metadata(self, content: str) -> Dict:
        """提取SKILL.md元数据"""
        metadata = {}

        # 匹配YAML frontmatter
        yaml_match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            for line in yaml_content.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")

                    if key == "tags":
                        value = [t.strip() for t in value.strip("[]").split(",")]

                    metadata[key] = value

        # 如果没有YAML,尝试从标题提取
        if not metadata.get("name"):
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if title_match:
                metadata["name"] = title_match.group(1).strip()

        return metadata

    def _extract_description(self, content: str) -> str:
        """提取描述"""
        # 移除YAML frontmatter
        content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)

        # 查找第一个非标题段落
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("---"):
                return line[:300]

        return "No description available"
