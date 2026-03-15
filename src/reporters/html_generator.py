#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML报告生成器
生成美观的监控报告
"""

import json
from datetime import datetime
from typing import List, Dict
from jinja2 import Template


class HTMLReportGenerator:
    """HTML报告生成器"""

    def generate(self, skills: List[Dict]) -> str:
        """
        生成HTML报告

        Args:
            skills: 技能列表

        Returns:
            HTML字符串
        """
        template = Template(self._get_template())

        # 统计数据
        stats = self._calculate_stats(skills)

        # 分类技能
        must_install = [
            s for s in skills if s.get("recommendation", {}).get("level") == "必装"
        ]
        optional = [
            s for s in skills if s.get("recommendation", {}).get("level") == "可选"
        ]
        not_recommended = [
            s for s in skills if s.get("recommendation", {}).get("level") == "不推荐"
        ]
        high_risk = [
            s for s in skills if s.get("security", {}).get("risk_level") == "HIGH"
        ]

        # 按兼容性排序
        fully_compat = [
            s for s in skills if s.get("compatibility", {}).get("level") == "完全兼容"
        ]
        partial_compat = [
            s for s in skills if s.get("compatibility", {}).get("level") == "部分兼容"
        ]

        html = template.render(
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
            stats=stats,
            all_skills=skills,
            must_install=must_install,
            optional=optional,
            not_recommended=not_recommended,
            high_risk=high_risk,
            fully_compat=fully_compat,
            partial_compat=partial_compat,
        )

        return html

    def _calculate_stats(self, skills: List[Dict]) -> Dict:
        """计算统计数据"""
        total = len(skills)
        if total == 0:
            return {
                "total": 0,
                "must_install": 0,
                "optional": 0,
                "not_recommended": 0,
                "fully_compat": 0,
                "partial_compat": 0,
                "high_risk": 0,
                "avg_score": 0,
            }

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
        partial_compat = sum(
            1 for s in skills if s.get("compatibility", {}).get("level") == "部分兼容"
        )
        high_risk = sum(
            1 for s in skills if s.get("security", {}).get("risk_level") == "HIGH"
        )

        # 计算平均分
        scores = [s.get("value", {}).get("score", 0) for s in skills]
        avg_score = sum(scores) / len(scores) if scores else 0

        return {
            "total": total,
            "must_install": must_install,
            "optional": optional,
            "not_recommended": not_recommended,
            "fully_compat": fully_compat,
            "partial_compat": partial_compat,
            "high_risk": high_risk,
            "avg_score": round(avg_score, 1),
        }

    def _get_template(self) -> str:
        """获取HTML模板"""
        return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI技能监控日报</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            padding: 40px 0;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .header .subtitle {
            opacity: 0.9;
            font-size: 1.1em;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            border-radius: 16px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-card .number {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-card .label {
            color: #666;
            margin-top: 5px;
            font-size: 0.9em;
        }
        .section {
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        .skill-grid {
            display: grid;
            gap: 15px;
        }
        .skill-card {
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s;
        }
        .skill-card:hover {
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .skill-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 10px;
        }
        .skill-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }
        .skill-source {
            font-size: 0.8em;
            color: #888;
            background: #f5f5f5;
            padding: 4px 8px;
            border-radius: 4px;
        }
        .skill-desc {
            color: #666;
            margin-bottom: 10px;
            line-height: 1.5;
        }
        .skill-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 10px;
        }
        .tag {
            font-size: 0.75em;
            padding: 4px 10px;
            border-radius: 20px;
            font-weight: 500;
        }
        .tag-recommend {
            background: #d4edda;
            color: #155724;
        }
        .tag-optional {
            background: #fff3cd;
            color: #856404;
        }
        .tag-not-recommend {
            background: #f8d7da;
            color: #721c24;
        }
        .tag-compat {
            background: #cce5ff;
            color: #004085;
        }
        .tag-risk {
            background: #f5c6cb;
            color: #721c24;
        }
        .tag-value {
            background: #e2e3e5;
            color: #383d41;
        }
        .skill-metrics {
            display: flex;
            gap: 20px;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }
        .metric {
            font-size: 0.85em;
            color: #666;
        }
        .metric strong {
            color: #333;
        }
        .risk-warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 0 8px 8px 0;
        }
        .risk-danger {
            background: #f8d7da;
            border-left: 4px solid #dc3545;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        .footer {
            text-align: center;
            color: rgba(255,255,255,0.7);
            padding: 20px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI技能监控日报</h1>
            <p class="subtitle">生成时间: {{ generated_at }}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="number">{{ stats.total }}</div>
                <div class="label">监控技能数</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ stats.must_install }}</div>
                <div class="label">必装推荐</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ stats.fully_compat }}</div>
                <div class="label">完全兼容</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ stats.high_risk }}</div>
                <div class="label">高风险警告</div>
            </div>
        </div>
        
        {% if high_risk %}
        <div class="section">
            <h2>⚠️ 高风险警告</h2>
            <div class="skill-grid">
                {% for skill in high_risk %}
                <div class="skill-card">
                    <div class="skill-header">
                        <span class="skill-name">{{ skill.name }}</span>
                        <span class="skill-source">{{ skill.source }}</span>
                    </div>
                    <div class="risk-warning risk-danger">
                        <strong>安全风险:</strong> {{ skill.security.mitigation }}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if must_install %}
        <div class="section">
            <h2>🔥 必装推荐</h2>
            <div class="skill-grid">
                {% for skill in must_install %}
                <div class="skill-card">
                    <div class="skill-header">
                        <span class="skill-name">{{ skill.name }}</span>
                        <span class="skill-source">{{ skill.source }}</span>
                    </div>
                    <div class="skill-desc">{{ skill.description[:200] }}{% if skill.description|length > 200 %}...{% endif %}</div>
                    
                    <div class="skill-tags">
                        <span class="tag tag-recommend">必装</span>
                        <span class="tag tag-compat">{{ skill.compatibility.level }}</span>
                        <span class="tag tag-value">评分: {{ skill.value.score }}/10</span>
                        {% for tag in skill.value.tags[:2] %}
                        <span class="tag tag-value">{{ tag }}</span>
                        {% endfor %}
                    </div>
                    
                    <div class="skill-metrics">
                        <span class="metric"><strong>作者:</strong> {{ skill.author }}</span>
                        <span class="metric"><strong>安全:</strong> {{ skill.security.risk_level }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if optional %}
        <div class="section">
            <h2>📦 可选安装</h2>
            <div class="skill-grid">
                {% for skill in optional %}
                <div class="skill-card">
                    <div class="skill-header">
                        <span class="skill-name">{{ skill.name }}</span>
                        <span class="skill-source">{{ skill.source }}</span>
                    </div>
                    <div class="skill-desc">{{ skill.description[:150] }}{% if skill.description|length > 150 %}...{% endif %}</div>
                    
                    <div class="skill-tags">
                        <span class="tag tag-optional">可选</span>
                        <span class="tag tag-compat">{{ skill.compatibility.level }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        <div class="section">
            <h2>📊 完整列表</h2>
            <div class="skill-grid">
                {% for skill in all_skills %}
                <div class="skill-card">
                    <div class="skill-header">
                        <span class="skill-name">{{ skill.name }}</span>
                        <span class="skill-source">{{ skill.source }}</span>
                    </div>
                    
                    <div class="skill-tags">
                        {% set level = skill.recommendation.level %}
                        {% if level == "必装" %}
                            <span class="tag tag-recommend">必装</span>
                        {% elif level == "可选" %}
                            <span class="tag tag-optional">可选</span>
                        {% else %}
                            <span class="tag tag-not-recommend">不推荐</span>
                        {% endif %}
                        
                        <span class="tag tag-compat">{{ skill.compatibility.level }}</span>
                        
                        {% if skill.security.risk_level == "HIGH" %}
                            <span class="tag tag-risk">高风险</span>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="footer">
            <p>AI Skills Monitor - 自动化技能监控与评估系统</p>
        </div>
    </div>
</body>
</html>
"""
