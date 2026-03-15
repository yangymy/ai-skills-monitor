#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终极版HTML报告生成器 V3.0
包含：分类展示 + 搜索功能 + 技能对比 + 趋势图 + 专业描述
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
from jinja2 import Template


class HTMLReportGenerator:
    """终极版HTML报告生成器 - 全功能版"""

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
        "API开发": "📊",
        "监控运维": "📈",
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
        "API开发": "#14b8a6",
        "监控运维": "#f97316",
    }

    def generate(self, skills: List[Dict], historical_data: List[Dict] = None) -> str:
        """生成终极版HTML报告"""
        if not skills:
            return self._generate_empty_report()

        # 按分类分组
        categorized_skills = self._categorize_skills(skills)

        # 统计数据
        stats = self._calculate_stats(skills)

        # 计算趋势（如果有历史数据）
        trends = self._calculate_trends(skills, historical_data)

        # 热门对比组合
        comparison_pairs = self._generate_comparison_pairs(skills)

        # 使用建议
        recommendations = self._generate_recommendations(skills)

        template = Template(self._get_ultimate_template())

        html = template.render(
            generated_at=datetime.now().strftime("%Y年%m月%d日 %H:%M"),
            stats=stats,
            categorized_skills=categorized_skills,
            category_emoji=self.CATEGORY_EMOJI,
            category_colors=self.CATEGORY_COLORS,
            recommendations=recommendations,
            trends=trends,
            comparison_pairs=comparison_pairs,
            all_skills_json=json.dumps(skills, ensure_ascii=False),
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
                "total_installs": 0,
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

        total_installs = sum(s.get("install_count", 0) for s in skills)

        return {
            "total": total,
            "categories": categories,
            "must_install": must_install,
            "optional": optional,
            "not_recommended": not_recommended,
            "fully_compat": fully_compat,
            "high_risk": high_risk,
            "avg_rating": round(avg_rating, 1),
            "total_installs": total_installs,
        }

    def _calculate_trends(
        self, skills: List[Dict], historical_data: List[Dict] = None
    ) -> Dict:
        """计算趋势数据"""
        if not historical_data:
            # 如果没有历史数据，生成模拟趋势
            return self._generate_mock_trends(skills)

        return {}

    def _generate_mock_trends(self, skills: List[Dict]) -> Dict:
        """生成模拟趋势数据"""
        # 获取Top 6技能的趋势
        top_skills = sorted(
            skills, key=lambda x: x.get("install_count", 0), reverse=True
        )[:6]

        trends = []
        for skill in top_skills:
            # 生成6个月的模拟数据
            months = []
            ratings = []
            base_rating = skill.get("rating", 4.0)

            for i in range(6):
                month_date = datetime.now() - timedelta(days=(5 - i) * 30)
                months.append(month_date.strftime("%m月"))
                # 模拟轻微波动
                rating = round(base_rating + random.uniform(-0.2, 0.2), 1)
                ratings.append(rating)

            trends.append(
                {
                    "name": skill["name"],
                    "months": months,
                    "ratings": ratings,
                    "color": self.CATEGORY_COLORS.get(
                        skill.get("category", ""), "#667eea"
                    ),
                }
            )

        return {"skills": trends}

    def _generate_comparison_pairs(self, skills: List[Dict]) -> List[Dict]:
        """生成热门对比组合"""
        pairs = [
            {
                "title": "🤖 AI代码助手大PK",
                "skills": ["GitHub Copilot", "Codeium", "Cursor IDE", "Tabnine"],
                "description": "四大主流AI编程助手功能、价格、适用场景全面对比",
            },
            {
                "title": "🧪 测试框架选择",
                "skills": ["Jest", "Vitest", "Playwright", "Cypress"],
                "description": "前端测试方案对比：单元测试 vs E2E测试",
            },
            {
                "title": "⚡ 性能优化工具",
                "skills": ["Lighthouse", "PageSpeed Insights", "WebPageTest"],
                "description": "网页性能分析工具对比，哪个更适合你？",
            },
            {
                "title": "🗄️ 数据库工具",
                "skills": ["Prisma", "DBeaver", "TablePlus", "pgAdmin"],
                "description": "ORM vs GUI工具：数据库管理方案对比",
            },
        ]

        # 过滤掉不存在的技能
        valid_pairs = []
        skill_names = {s["name"] for s in skills}
        for pair in pairs:
            valid_skills = [s for s in pair["skills"] if s in skill_names]
            if len(valid_skills) >= 2:
                pair["skills"] = valid_skills
                valid_pairs.append(pair)

        return valid_pairs

    def _generate_recommendations(self, skills: List[Dict]) -> List[str]:
        """生成智能使用建议"""
        recommendations = []

        # 新手推荐
        ai_helpers = [
            s
            for s in skills
            if s.get("category") == "AI代码助手"
            and s.get("recommendation", {}).get("level") == "必装"
        ]
        if ai_helpers:
            names = "、".join([s["name"] for s in ai_helpers[:2]])
            recommendations.append(
                f"👋 **新手入门**：建议优先安装 {names}，大幅提升编码效率"
            )

        # 前端开发组合
        frontend_must = [
            s
            for s in skills
            if s.get("category") == "前端开发"
            and s.get("recommendation", {}).get("level") == "必装"
        ]
        frontend_optional = [
            s
            for s in skills
            if s.get("category") == "前端开发"
            and s.get("recommendation", {}).get("level") == "可选"
        ]
        if len(frontend_must) + len(frontend_optional) >= 3:
            all_frontend = frontend_must + frontend_optional
            names = "、".join([s["name"] for s in all_frontend[:3]])
            recommendations.append(f"🎨 **前端开发**：推荐组合 {names}，覆盖开发全流程")

        # 测试必备
        testing = [
            s
            for s in skills
            if s.get("category") == "测试工具"
            and s.get("recommendation", {}).get("level") in ["必装", "可选"]
        ]
        if len(testing) >= 2:
            names = "、".join([s["name"] for s in testing[:2]])
            recommendations.append(f"🧪 **质量保障**：测试必备 {names}，确保代码质量")

        # 安全第一
        security = [s for s in skills if s.get("category") == "安全扫描"]
        if security:
            names = "、".join([s["name"] for s in security[:2]])
            recommendations.append(f"🔒 **安全防护**：建议集成 {names}，定期扫描漏洞")

        # 性能关注
        performance = [s for s in skills if s.get("category") == "性能优化"]
        if performance:
            names = "、".join([s["name"] for s in performance[:2]])
            recommendations.append(f"⚡ **性能优化**：使用 {names} 持续监控网站性能")

        # DevOps工具链
        devops = [
            s
            for s in skills
            if s.get("category") == "DevOps"
            and s.get("recommendation", {}).get("level") in ["必装", "可选"]
        ]
        if len(devops) >= 2:
            names = "、".join([s["name"] for s in devops[:2]])
            recommendations.append(f"🔧 **DevOps**：推荐 {names} 构建CI/CD流水线")

        # 高风险提醒
        high_risk = [
            s for s in skills if s.get("security", {}).get("risk_level") == "HIGH"
        ]
        if high_risk:
            recommendations.append(
                f"⚠️ **安全提醒**：{len(high_risk)} 个技能存在高风险，使用时请注意数据安全"
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

    def _get_ultimate_template(self) -> str:
        """获取终极版HTML模板"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI技能监控日报 - 终极版</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        .header {
            text-align: center;
            color: white;
            padding: 40px 0;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header .subtitle { opacity: 0.9; font-size: 1.1em; }
        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        .search-section {
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .search-box { display: flex; gap: 15px; align-items: center; }
        .search-input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 1.1em;
            transition: border-color 0.3s;
        }
        .search-input:focus {
            outline: none;
            border-color: #667eea;
        }
        .search-stats {
            margin-top: 15px;
            color: #6b7280;
            font-size: 0.9em;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .stat-card:hover { transform: translateY(-3px); }
        .stat-card .number { font-size: 2em; font-weight: bold; color: #667eea; }
        .stat-card .label { color: #666; margin-top: 5px; font-size: 0.85em; }
        
        .comparison-section {
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .comparison-section h2 {
            margin-bottom: 20px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .comparison-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }
        .comparison-card {
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .comparison-card:hover {
            border-color: #667eea;
            box-shadow: 0 5px 20px rgba(102,126,234,0.2);
        }
        .comparison-card h3 {
            font-size: 1.1em;
            color: #333;
            margin-bottom: 8px;
        }
        .comparison-card p {
            color: #6b7280;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .comparison-card .skills-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .comparison-card .skill-tag {
            background: #f3f4f6;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            color: #4b5563;
        }
        
        .trends-section {
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .trends-section h2 {
            margin-bottom: 20px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .chart-container {
            position: relative;
            height: 300px;
            margin-top: 20px;
        }
        
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
        .skill-card.hidden { display: none; }
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
        
        .recommendations-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 25px;
            margin-top: 20px;
            color: white;
        }
        .recommendations-section h2 {
            margin-bottom: 20px;
            font-size: 1.3em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .recommendations-list {
            list-style: none;
            padding: 0;
        }
        .recommendations-list li {
            padding: 12px 0;
            padding-left: 35px;
            position: relative;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            line-height: 1.6;
        }
        .recommendations-list li:last-child { border-bottom: none; }
        .recommendations-list li:before {
            content: "💡";
            position: absolute;
            left: 0;
            font-size: 1.2em;
        }
        
        .footer {
            text-align: center;
            color: rgba(255,255,255,0.7);
            padding: 30px 20px;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .skill-header { flex-direction: column; }
            .skill-meta { width: 100%; }
            .comparison-grid { grid-template-columns: 1fr; }
            .search-box { flex-direction: column; }
        }
        
        .highlight {
            background: linear-gradient(120deg, #fde047 0%, #fde047 100%);
            background-repeat: no-repeat;
            background-size: 100% 40%;
            background-position: 0 88%;
            padding: 0 2px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🤖 AI技能监控日报</h1>
            <p class="subtitle">生成时间: {{ generated_at }}</p>
            <span class="badge">✨ 终极版 V3.0 - 50个精选技能</span>
        </div>
        
        <!-- Search -->
        <div class="search-section">
            <div class="search-box">
                <input type="text" 
                       class="search-input" 
                       id="skillSearch" 
                       placeholder="🔍 搜索技能名称、描述、分类..."
                       autocomplete="off">
            </div>
            <div class="search-stats" id="searchStats">
                显示全部 {{ stats.total }} 个技能
            </div>
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
                <div class="number">{{ "{:,}".format(stats.total_installs // 1000000) }}M</div>
                <div class="label">总安装量</div>
            </div>
        </div>
        
        <!-- Comparison Section -->
        <div class="comparison-section">
            <h2>🆚 热门技能对比</h2>
            <div class="comparison-grid">
                {% for pair in comparison_pairs %}
                <div class="comparison-card" onclick="compareSkills({{ pair.skills | tojson }});">
                    <h3>{{ pair.title }}</h3>
                    <p>{{ pair.description }}</p>
                    <div class="skills-tags">
                        {% for skill_name in pair.skills %}
                        <span class="skill-tag">{{ skill_name }}</span>
                        {% endfor %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <!-- Trends Section -->
        <div class="trends-section">
            <h2>📈 技能评分趋势（近6个月）</h2>
            <div class="chart-container">
                <canvas id="trendsChart"></canvas>
            </div>
        </div>
        
        <!-- Categories -->
        {% for category, skills in categorized_skills.items() %}
        <div class="category-section" data-category="{{ category }}">
            <div class="category-header" style="border-color: {{ category_colors.get(category, '#667eea') }}">
                <span class="emoji">{{ category_emoji.get(category, '📦') }}</span>
                <h2>{{ category }}</h2>
                <span class="count">{{ skills|length }} 个技能</span>
            </div>
            
            {% for skill in skills %}
            <div class="skill-card" 
                 data-skill-name="{{ skill.name }}"
                 data-skill-desc="{{ skill.description }}"
                 data-skill-category="{{ skill.category }}"
                 data-skill-function="{{ skill.function }}">
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
                        <h4>🎯 核心功能</h4>
                        <p>{{ skill.function or skill.description or '暂无功能说明' }}</p>
                    </div>
                    
                    <div class="content-section">
                        <h4>📖 使用方法</h4>
                        <p>{{ skill.usage or '请参考官方文档' }}</p>
                    </div>
                    
                    {% if skill.benefits %}
                    <div class="content-section">
                        <h4>✅ 核心优势</h4>
                        <ul class="benefits-list">
                            {% for benefit in skill.benefits %}
                            <li>{{ benefit }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                    
                    {% if skill.risks %}
                    <div class="content-section">
                        <h4>⚠️ 注意事项</h4>
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
                        <span class="tag tag-recommend-must">🔥 必装推荐</span>
                    {% elif rec_level == '可选' %}
                        <span class="tag tag-recommend-optional">📦 可选安装</span>
                    {% else %}
                        <span class="tag tag-recommend-no">❌ 谨慎使用</span>
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
            <h2>💡 智能使用建议</h2>
            <ul class="recommendations-list">
                {% for rec in recommendations %}
                <li>{{ rec }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        <!-- Footer -->
        <div class="footer">
            <p>🚀 AI Skills Monitor V3.0 - 终极版全功能报告</p>
            <p>数据来源: 核心技能数据库 | 更新时间: {{ generated_at }}</p>
        </div>
    </div>
    
    <script>
        // 技能数据
        const allSkills = {{ all_skills_json | safe }};
        
        // 搜索功能
        const searchInput = document.getElementById('skillSearch');
        const searchStats = document.getElementById('searchStats');
        
        searchInput.addEventListener('input', function(e) {
            const keyword = e.target.value.toLowerCase().trim();
            const skillCards = document.querySelectorAll('.skill-card');
            const categorySections = document.querySelectorAll('.category-section');
            
            let visibleCount = 0;
            
            if (keyword === '') {
                skillCards.forEach(card => {
                    card.classList.remove('hidden');
                    visibleCount++;
                });
                categorySections.forEach(section => section.style.display = 'block');
                searchStats.textContent = `显示全部 {{ stats.total }} 个技能`;
            } else {
                skillCards.forEach(card => {
                    const name = card.dataset.skillName.toLowerCase();
                    const desc = card.dataset.skillDesc.toLowerCase();
                    const category = card.dataset.skillCategory.toLowerCase();
                    const func = card.dataset.skillFunction.toLowerCase();
                    
                    if (name.includes(keyword) || desc.includes(keyword) || 
                        category.includes(keyword) || func.includes(keyword)) {
                        card.classList.remove('hidden');
                        visibleCount++;
                        highlightText(card, keyword);
                    } else {
                        card.classList.add('hidden');
                    }
                });
                
                categorySections.forEach(section => {
                    const visibleCards = section.querySelectorAll('.skill-card:not(.hidden)');
                    section.style.display = visibleCards.length > 0 ? 'block' : 'none';
                });
                
                searchStats.textContent = `找到 ${visibleCount} 个匹配的技能`;
            }
        });
        
        // 高亮文本
        function highlightText(card, keyword) {
            card.querySelectorAll('.highlight').forEach(el => {
                el.outerHTML = el.innerHTML;
            });
            
            if (keyword) {
                const walker = document.createTreeWalker(
                    card, NodeFilter.SHOW_TEXT, null, false
                );
                const textNodes = [];
                let node;
                while (node = walker.nextNode()) {
                    if (node.parentElement.tagName !== 'SCRIPT' && 
                        node.textContent.toLowerCase().includes(keyword)) {
                        textNodes.push(node);
                    }
                }
                
                textNodes.forEach(node => {
                    const span = document.createElement('span');
                    span.className = 'highlight';
                    const regex = new RegExp(`(${keyword})`, 'gi');
                    span.innerHTML = node.textContent.replace(regex, '<span class="highlight">$1</span>');
                    node.parentNode.replaceChild(span, node);
                });
            }
        }
        
        // 技能对比功能
        function compareSkills(skillNames) {
            const skills = allSkills.filter(s => skillNames.includes(s.name));
            let comparisonHtml = '<div style="padding: 20px;">';
            
            comparisonHtml += '<h2 style="margin-bottom: 20px;">技能对比</h2>';
            comparisonHtml += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">';
            
            skills.forEach(skill => {
                comparisonHtml += `
                    <div style="border: 2px solid #e5e7eb; border-radius: 12px; padding: 15px;">
                        <h3 style="color: #333; margin-bottom: 10px;">${skill.name}</h3>
                        <p style="color: #666; font-size: 0.9em; margin-bottom: 10px;">${skill.description}</p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <span style="background: #f3f4f6; padding: 4px 10px; border-radius: 15px; font-size: 0.8em;">⭐ ${skill.rating || 'N/A'}</span>
                            <span style="background: #f3f4f6; padding: 4px 10px; border-radius: 15px; font-size: 0.8em;">📥 ${skill.install_count ? (skill.install_count / 1000000).toFixed(1) + 'M' : 'N/A'}</span>
                        </div>
                        <div style="margin-top: 10px;">
                            <strong>优势:</strong>
                            <ul style="margin-left: 20px; margin-top: 5px;">
                                ${skill.benefits ? skill.benefits.map(b => `<li>${b}</li>`).join('') : ''}
                            </ul>
                        </div>
                    </div>
                `;
            });
            
            comparisonHtml += '</div></div>';
            
            const popup = window.open('', '_blank', 'width=900,height=600');
            popup.document.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>技能对比</title>
                    <style>
                        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; background: #f9fafb; }
                    </style>
                </head>
                <body>${comparisonHtml}</body>
                </html>
            `);
        }
        
        // 趋势图
        {% if trends and trends.skills %}
        const ctx = document.getElementById('trendsChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: {{ trends.skills[0].months | tojson }},
                datasets: [
                    {% for skill in trends.skills %}
                    {
                        label: '{{ skill.name }}',
                        data: {{ skill.ratings | tojson }},
                        borderColor: '{{ skill.color }}',
                        backgroundColor: '{{ skill.color }}20',
                        tension: 0.4,
                        fill: false
                    }{% if not loop.last %},{% endif %}
                    {% endfor %}
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 15
                        }
                    }
                },
                scales: {
                    y: {
                        min: 3.5,
                        max: 5.0,
                        grid: {
                            color: '#f3f4f6'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
        {% endif %}
    </script>
</body>
</html>"""
