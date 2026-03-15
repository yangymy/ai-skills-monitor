#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版HTML报告生成器 - 中文详细分析
"""

import json
from datetime import datetime
from typing import List, Dict
from jinja2 import Template


class HTMLReportGenerator:
    """增强版HTML报告生成器"""

    def generate(self, skills: List[Dict]) -> str:
        """生成详细的HTML报告"""
        if not skills:
            return self._generate_empty_report()

        template = Template(self._get_enhanced_template())

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

        html = template.render(
            generated_at=datetime.now().strftime("%Y年%m月%d日 %H:%M"),
            stats=stats,
            all_skills=skills,
            must_install=must_install,
            optional=optional,
            not_recommended=not_recommended,
            high_risk=high_risk,
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
        high_risk = sum(
            1 for s in skills if s.get("security", {}).get("risk_level") == "HIGH"
        )

        scores = [s.get("value", {}).get("score", 0) for s in skills]
        avg_score = sum(scores) / len(scores) if scores else 0

        return {
            "total": total,
            "must_install": must_install,
            "optional": optional,
            "not_recommended": not_recommended,
            "fully_compat": fully_compat,
            "high_risk": high_risk,
            "avg_score": round(avg_score, 1),
        }

    def _generate_empty_report(self) -> str:
        """生成空报告"""
        return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>AI技能监控日报</title></head>
<body style="font-family: Arial, sans-serif; padding: 40px;">
<h1>AI技能监控日报</h1>
<p>本次监控未获取到新的技能数据。</p>
<p>可能原因：</p>
<ul>
<li>监控的仓库近期没有更新</li>
<li>GitHub API限制（未设置token或达到限额）</li>
<li>网络连接问题</li>
</ul>
</body></html>"""

    def _get_enhanced_template(self) -> str:
        """获取增强版HTML模板"""
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
        .header {
            text-align: center;
            color: white;
            padding: 40px 0;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
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
        }
        .stat-card .number { font-size: 2.5em; font-weight: bold; color: #667eea; }
        .stat-card .label { color: #666; margin-top: 5px; font-size: 0.9em; }
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
        .skill-card {
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }
        .skill-card:hover { box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
        .skill-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 10px;
        }
        .skill-name { font-size: 1.3em; font-weight: bold; color: #333; }
        .skill-source {
            font-size: 0.8em;
            color: #888;
            background: #f5f5f5;
            padding: 4px 8px;
            border-radius: 4px;
        }
        .skill-section { margin: 15px 0; }
        .skill-section h4 { color: #667eea; margin-bottom: 8px; font-size: 0.95em; }
        .skill-section p { color: #555; line-height: 1.6; font-size: 0.9em; }
        .skill-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 0;
        }
        .tag {
            font-size: 0.75em;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 500;
        }
        .tag-recommend { background: #d4edda; color: #155724; }
        .tag-optional { background: #fff3cd; color: #856404; }
        .tag-not-recommend { background: #f8d7da; color: #721c24; }
        .tag-compat { background: #cce5ff; color: #004085; }
        .tag-risk { background: #f5c6cb; color: #721c24; }
        .pros-cons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 10px;
        }
        .pros { background: #f0f9eb; padding: 12px; border-radius: 8px; }
        .cons { background: #fef0f0; padding: 12px; border-radius: 8px; }
        .pros h5 { color: #67c23a; margin-bottom: 8px; }
        .cons h5 { color: #f56c6c; margin-bottom: 8px; }
        .code-example {
            background: #f5f7fa;
            padding: 12px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            overflow-x: auto;
            margin-top: 8px;
        }
        .risk-warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 0 8px 8px 0;
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
            {% for skill in high_risk %}
            <div class="skill-card">
                <div class="skill-header">
                    <span class="skill-name">{{ skill.name }}</span>
                    <span class="skill-source">{{ skill.source }}</span>
                </div>
                <div class="risk-warning">
                    <strong>安全风险:</strong> {{ skill.security.mitigation }}
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if must_install %}
        <div class="section">
            <h2>🔥 必装推荐技能</h2>
            {% for skill in must_install %}
            <div class="skill-card">
                <div class="skill-header">
                    <span class="skill-name">{{ skill.name }}</span>
                    <span class="skill-source">{{ skill.source }}</span>
                </div>
                
                <div class="skill-section">
                    <h4>📋 功能描述</h4>
                    <p>{{ skill.description or '暂无描述' }}</p>
                </div>
                
                <div class="skill-section">
                    <h4>🎯 作用与价值</h4>
                    <p>{{ skill.value.summary or '该技能能够提升开发效率，简化工作流程' }}</p>
                </div>
                
                {% if skill.examples %}
                <div class="skill-section">
                    <h4>💡 使用示例</h4>
                    <div class="code-example">{{ skill.examples[:500] }}</div>
                </div>
                {% endif %}
                
                <div class="pros-cons">
                    <div class="pros">
                        <h5>✅ 好处</h5>
                        <p>{{ skill.value.pros or '• 提升效率<br>• 简化操作' }}</p>
                    </div>
                    <div class="cons">
                        <h5>⚠️ 注意事项</h5>
                        <p>{{ skill.value.cons or '• 暂无已知问题' }}</p>
                    </div>
                </div>
                
                <div class="skill-tags">
                    <span class="tag tag-recommend">必装</span>
                    <span class="tag tag-compat">{{ skill.compatibility.level }}</span>
                    <span class="tag">评分: {{ skill.value.score }}/10</span>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <div class="footer">
            <p>AI Skills Monitor - 智能技能监控与评估系统</p>
        </div>
    </div>
</body>
</html>"""
