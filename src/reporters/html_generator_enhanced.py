#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版HTML报告生成器 - 按分类展示技能详情
"""

import json
from datetime import datetime
from typing import List, Dict
from jinja2 import Template


class HTMLReportGenerator:
    """增强版HTML报告生成器 - 分类展示"""

    # 分类 emoji 映射
    CATEGORY_EMOJI = {
        "AI代码助手": "🤖",
        "文档生成": "📝",
        "测试工具": "🧪",
        "安全扫描": "🔒",
        "性能优化": "⚡",
        "前端开发": "🎨",
        "数据库": "🗄️",
        "DevOps": "🔧",
    }

    # 分类颜色映射
    CATEGORY_COLORS = {
        "AI代码助手": "#667eea",
        "文档生成": "#10b981",
        "测试工具": "#f59e0b",
        "安全扫描": "#ef4444",
        "性能优化": "#8b5cf6",
        "前端开发": "#ec4899",
        "数据库": "#06b6d4",
        "DevOps": "#6366f1",
    }

    def generate(self, skills: List[Dict]) -> str:
        """生成详细的分类HTML报告"""
        if not skills:
            return self._generate_empty_report()

        # 按分类分组技能
        categorized_skills = self._categorize_skills(skills)

        # 统计数据
        stats = self._calculate_stats(skills)

        # 使用建议
        recommendations = self._generate_recommendations(skills)

        template = Template(self._get_categorized_template())

        html = template.render(
            generated_at=datetime.now().strftime("%Y年%m月%d日 %H:%M"),
            stats=stats,
            categorized_skills=categorized_skills,
            category_emoji=self.CATEGORY_EMOJI,
            category_colors=self.CATEGORY_COLORS,
            recommendations=recommendations,
        )

        return html

    def _categorize_skills(self, skills: List[Dict]) -> Dict[str, List[Dict]]:
        """按分类分组技能"""
        categorized = {}
        for skill in skills:
            category = skill.get("category", "其他")
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(skill)

        # 按分类名称排序
        return dict(sorted(categorized.items()))

    def _calculate_stats(self, skills: List[Dict]) -> Dict:
        """计算统计数据"""
        total = len(skills)
        if total == 0:
            return {
                "total": 0,
                "categories": 0,
                "must_install": 0,
                "optional": 0,
                "not_recommended": 0,
                "fully_compat": 0,
                "high_risk": 0,
                "avg_rating": 0,
            }

        categories = len(set(s.get("category", "") for s in skills))
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

        ratings = [s.get("rating", 0) for s in skills if s.get("rating")]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0

        return {
            "total": total,
            "categories": categories,
            "must_install": must_install,
            "optional": optional,
            "not_recommended": not_recommended,
            "fully_compat": fully_compat,
            "high_risk": high_risk,
            "avg_rating": round(avg_rating, 1),
        }

    def _generate_recommendations(self, skills: List[Dict]) -> List[str]:
        """生成使用建议"""
        recommendations = []

        # 找出必装的AI代码助手
        ai_helpers = [
            s
            for s in skills
            if s.get("category") == "AI代码助手"
            and s.get("recommendation", {}).get("level") == "必装"
        ]
        if ai_helpers:
            names = ", ".join([s["name"] for s in ai_helpers[:2]])
            recommendations.append(f"💡 首次使用建议安装 AI 代码助手: {names}")

        # 前端开发组合
        frontend = [
            s
            for s in skills
            if s.get("category") == "前端开发"
            and s.get("recommendation", {}).get("level") in ["必装", "可选"]
        ]
        if len(frontend) >= 3:
            names = ", ".join([s["name"] for s in frontend[:3]])
            recommendations.append(f"🎨 前端开发推荐组合: {names}")

        # 测试必备
        testing = [s for s in skills if s.get("category") == "测试工具"]
        if testing:
            names = ", ".join([s["name"] for s in testing[:2]])
            recommendations.append(f"🧪 测试必备工具: {names}")

        # 安全扫描
        security = [s for s in skills if s.get("category") == "安全扫描"]
        if security:
            recommendations.append(f"🔒 建议定期运行安全扫描工具检查项目漏洞")

        # 高风险提醒
        high_risk = [
            s for s in skills if s.get("security", {}).get("risk_level") == "HIGH"
        ]
        if high_risk:
            recommendations.append(
                f"⚠️ 注意: {len(high_risk)} 个技能存在安全风险，请谨慎使用"
            )

        return recommendations

    def _generate_empty_report(self) -> str:
        """生成空报告"""
        return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>AI技能监控日报</title></head>
<body style="font-family: Arial, sans-serif; padding: 40px;">
<h1>🤖 AI技能监控日报</h1>
<p>本次监控未获取到技能数据。</p>
<p>请检查系统配置。</p>
</body></html>"""

    def _get_categorized_template(self) -> str:
        """获取分类展示HTML模板"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI技能监控日报</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        
        /* Header */
        .header {
            text-align: center;
            color: white;
            padding: 40px 0;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header .subtitle { opacity: 0.9; font-size: 1.1em; }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .stat-card .number { font-size: 2em; font-weight: bold; color: #667eea; }
        .stat-card .label { color: #666; margin-top: 5px; font-size: 0.85em; }
        
        /* Category Section */
        .category-section {
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .category-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid;
        }
        .category-header .emoji { font-size: 1.8em; margin-right: 10px; }
        .category-header h2 { font-size: 1.5em; color: #333; }
        .category-header .count {
            margin-left: auto;
            background: #f3f4f6;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            color: #666;
        }
        
        /* Skill Card */
        .skill-card {
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s;
            background: #fafafa;
        }
        .skill-card:hover { 
            box-shadow: 0 5px 20px rgba(0,0,0,0.1); 
            transform: translateY(-2px);
        }
        .skill-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 10px;
        }
        .skill-name { 
            font-size: 1.2em; 
            font-weight: bold; 
            color: #1f2937;
        }
        .skill-meta {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .meta-item {
            font-size: 0.8em;
            color: #6b7280;
            background: #f3f4f6;
            padding: 4px 10px;
            border-radius: 6px;
        }
        .meta-item .label { color: #9ca3af; margin-right: 4px; }
        
        /* Skill Content */
        .skill-content { margin-top: 15px; }
        .content-section { margin-bottom: 12px; }
        .content-section h4 {
            font-size: 0.9em;
            color: #4b5563;
            margin-bottom: 6px;
            font-weight: 600;
        }
        .content-section p {
            color: #6b7280;
            line-height: 1.6;
            font-size: 0.9em;
        }
        
        /* Lists */
        .benefits-list, .risks-list {
            list-style: none;
            padding: 0;
        }
        .benefits-list li {
            padding: 4px 0;
            padding-left: 20px;
            position: relative;
            color: #059669;
            font-size: 0.9em;
        }
        .benefits-list li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #10b981;
            font-weight: bold;
        }
        .risks-list li {
            padding: 4px 0;
            padding-left: 20px;
            position: relative;
            color: #dc2626;
            font-size: 0.9em;
        }
        .risks-list li:before {
            content: "⚠";
            position: absolute;
            left: 0;
            color: #f59e0b;
        }
        
        /* Tags */
        .skill-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e5e7eb;
        }
        .tag {
            font-size: 0.75em;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: 500;
        }
        .tag-recommend-must { background: #d1fae5; color: #065f46; }
        .tag-recommend-optional { background: #fef3c7; color: #92400e; }
        .tag-recommend-no { background: #fee2e2; color: #991b1b; }
        .tag-compat-full { background: #dbeafe; color: #1e40af; }
        .tag-compat-partial { background: #fef9c3; color: #854d0e; }
        .tag-risk { background: #fecaca; color: #991b1b; }
        .tag-source {
            background: #f3f4f6;
            color: #4b5563;
        }
        
        /* Recommendations Section */
        .recommendations-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 25px;
            margin-top: 20px;
            color: white;
        }
        .recommendations-section h2 {
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .recommendations-list {
            list-style: none;
            padding: 0;
        }
        .recommendations-list li {
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .recommendations-list li:last-child { border-bottom: none; }
        .recommendations-list li:before {
            content: "💡";
            position: absolute;
            left: 0;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: rgba(255,255,255,0.7);
            padding: 30px 20px;
            font-size: 0.9em;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .skill-header { flex-direction: column; }
            .skill-meta { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🤖 AI技能监控日报</h1>
            <p class="subtitle">生成时间: {{ generated_at }}</p>
        </div>
        
        <!-- Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="number">{{ stats.total }}</div>
                <div class="label">总技能数</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ stats.categories }}</div>
                <div class="label">分类数量</div>
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
                <div class="number">{{ stats.avg_rating }}</div>
                <div class="label">平均评分</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ stats.high_risk }}</div>
                <div class="label">高风险</div>
            </div>
        </div>
        
        <!-- Categories -->
        {% for category, skills in categorized_skills.items() %}
        <div class="category-section">
            <div class="category-header" style="border-color: {{ category_colors.get(category, '#667eea') }}">
                <span class="emoji">{{ category_emoji.get(category, '📦') }}</span>
                <h2>{{ category }}</h2>
                <span class="count">{{ skills|length }} 个技能</span>
            </div>
            
            {% for skill in skills %}
            <div class="skill-card">
                <div class="skill-header">
                    <span class="skill-name">{{ skill.name }}</span>
                    <div class="skill-meta">
                        <span class="meta-item">
                            <span class="label">⭐</span>{{ skill.rating or 'N/A' }}
                        </span>
                        <span class="meta-item">
                            <span class="label">📥</span>{{ "{:,}".format(skill.install_count) if skill.install_count else 'N/A' }}
                        </span>
                    </div>
                </div>
                
                <div class="skill-content">
                    <div class="content-section">
                        <h4>📝 简介</h4>
                        <p>{{ skill.description or '暂无描述' }}</p>
                    </div>
                    
                    <div class="content-section">
                        <h4>🎯 功能</h4>
                        <p>{{ skill.function or skill.description or '暂无功能说明' }}</p>
                    </div>
                    
                    <div class="content-section">
                        <h4>📖 使用方法</h4>
                        <p>{{ skill.usage or '请参考官方文档' }}</p>
                    </div>
                    
                    {% if skill.benefits %}
                    <div class="content-section">
                        <h4>✅ 好处</h4>
                        <ul class="benefits-list">
                            {% for benefit in skill.benefits %}
                            <li>{{ benefit }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                    
                    {% if skill.risks %}
                    <div class="content-section">
                        <h4>⚠️ 风险/注意事项</h4>
                        <ul class="risks-list">
                            {% for risk in skill.risks %}
                            <li>{{ risk }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                </div>
                
                <div class="skill-tags">
                    {% set rec_level = skill.recommendation.level if skill.recommendation else '未知' %}
                    {% if rec_level == '必装' %}
                        <span class="tag tag-recommend-must">🔥 必装</span>
                    {% elif rec_level == '可选' %}
                        <span class="tag tag-recommend-optional">📦 可选</span>
                    {% else %}
                        <span class="tag tag-recommend-no">❌ 不推荐</span>
                    {% endif %}
                    
                    {% set compat_level = skill.compatibility.level if skill.compatibility else skill.compatibility %}
                    {% if compat_level == '完全兼容' %}
                        <span class="tag tag-compat-full">✅ 完全兼容</span>
                    {% else %}
                        <span class="tag tag-compat-partial">⚡ {{ compat_level }}</span>
                    {% endif %}
                    
                    {% if skill.security and skill.security.risk_level == 'HIGH' %}
                        <span class="tag tag-risk">🚨 高风险</span>
                    {% endif %}
                    
                    <span class="tag tag-source">📎 {{ skill.source }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endfor %}
        
        <!-- Recommendations -->
        {% if recommendations %}
        <div class="recommendations-section">
            <h2>💡 使用建议</h2>
            <ul class="recommendations-list">
                {% for rec in recommendations %}
                <li>{{ rec }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        <!-- Footer -->
        <div class="footer">
            <p>AI Skills Monitor - 智能技能监控与评估系统</p>
            <p>数据来源: 核心技能数据库 (预设模式)</p>
        </div>
    </div>
</body>
</html>"""
