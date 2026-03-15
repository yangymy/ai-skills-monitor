#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skills.sh 技能获取器
从skills.sh平台获取技能
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional


class SkillsShFetcher:
    """skills.sh技能获取器"""

    def __init__(self, base_url: str = "https://skills.sh"):
        """
        初始化

        Args:
            base_url: skills.sh基础URL
        """
        self.base_url = base_url
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "AI-Skills-Monitor/1.0",
        }

    def fetch_trending(self, limit: int = 20) -> List[Dict]:
        """
        获取热门技能

        Args:
            limit: 返回数量

        Returns:
            技能列表
        """
        skills = []

        # 尝试多种API端点
        endpoints = [
            f"{self.base_url}/api/skills?trending=24h&limit={limit}",
            f"{self.base_url}/api/skills?sort=updated&limit={limit}",
            f"{self.base_url}/api/v1/skills/popular",
        ]

        for url in endpoints:
            try:
                data = self._fetch_with_fallback(url)
                if data:
                    parsed = self._parse_response(data)
                    skills.extend(parsed)
                    break  # 成功获取后退出
            except Exception as e:
                print(f"Endpoint failed {url}: {e}")
                continue

        # 如果API都失败,尝试页面抓取
        if not skills:
            skills = self._scrape_webpage()

        return skills[:limit]

    def _fetch_with_fallback(self, url: str) -> Optional[Dict]:
        """获取数据,支持多种格式"""
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)

            if resp.status_code != 200:
                return None

            content_type = resp.headers.get("Content-Type", "")

            if "application/json" in content_type:
                return resp.json()
            else:
                # 尝试解析HTML或文本
                return {"html": resp.text}

        except Exception as e:
            print(f"Fetch error: {e}")
            return None

    def _parse_response(self, data: Dict) -> List[Dict]:
        """解析API响应"""
        skills = []

        # 处理不同格式的响应
        if isinstance(data, list):
            skill_list = data
        elif isinstance(data, dict):
            # 可能的键名
            for key in ["skills", "data", "results", "items"]:
                if key in data:
                    skill_list = data[key]
                    break
            else:
                skill_list = [data] if "name" in data else []
        else:
            return skills

        for item in skill_list:
            skill = self._normalize_skill(item)
            if skill:
                skills.append(skill)

        return skills

    def _normalize_skill(self, item: Dict) -> Optional[Dict]:
        """标准化技能数据"""
        if not isinstance(item, dict):
            return None

        name = item.get("name") or item.get("title") or item.get("id")
        if not name:
            return None

        return {
            "name": name,
            "description": item.get("description", item.get("summary", ""))[:300],
            "author": item.get(
                "author", item.get("creator", item.get("namespace", ""))
            ),
            "version": item.get("version", "1.0.0"),
            "tags": item.get("tags", item.get("categories", [])),
            "install_count": item.get("installs", item.get("downloads", 0)),
            "updated_at": item.get(
                "updated_at", item.get("last_updated", datetime.now().isoformat())
            ),
            "source": "skills.sh",
            "url": item.get(
                "url", item.get("html_url", f"{self.base_url}/skills/{name}")
            ),
            "raw_content": json.dumps(item, ensure_ascii=False)[:2000],
        }

    def _scrape_webpage(self) -> List[Dict]:
        """
        从网页抓取技能列表(备用方案)
        """
        skills = []

        try:
            from bs4 import BeautifulSoup

            resp = requests.get(f"{self.base_url}/", headers=self.headers, timeout=30)
            if resp.status_code != 200:
                return skills

            soup = BeautifulSoup(resp.text, "html.parser")

            # 查找技能卡片(根据实际页面结构调整选择器)
            skill_cards = soup.find_all(
                ["article", "div", "li"], class_=lambda x: x and "skill" in x.lower()
            )

            for card in skill_cards[:20]:
                try:
                    name_elem = card.find(["h2", "h3", "h4", "a"])
                    desc_elem = card.find(
                        ["p", "div"], class_=lambda x: x and "desc" in x.lower()
                    )

                    name = name_elem.get_text(strip=True) if name_elem else "Unknown"
                    description = (
                        desc_elem.get_text(strip=True)[:300] if desc_elem else ""
                    )

                    skill = {
                        "name": name,
                        "description": description,
                        "author": "skills.sh",
                        "version": "1.0.0",
                        "tags": [],
                        "updated_at": datetime.now().isoformat(),
                        "source": "skills.sh",
                        "url": f"{self.base_url}/skills/{name}",
                        "raw_content": str(card)[:1000],
                    }

                    skills.append(skill)
                except Exception:
                    continue

        except ImportError:
            print("BeautifulSoup not available for web scraping")
        except Exception as e:
            print(f"Web scraping error: {e}")

        return skills

    def search_skills(self, query: str, limit: int = 10) -> List[Dict]:
        """
        搜索技能

        Args:
            query: 搜索关键词
            limit: 返回数量

        Returns:
            技能列表
        """
        try:
            url = f"{self.base_url}/api/skills/search"
            params = {"q": query, "limit": limit}

            resp = requests.get(url, headers=self.headers, params=params, timeout=30)

            if resp.status_code == 200:
                data = resp.json()
                return self._parse_response(data)

        except Exception as e:
            print(f"Search error: {e}")

        return []
