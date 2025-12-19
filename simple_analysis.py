import csv
import math

# 데이터 읽기
data = []
with open('discount_sales_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['상품명']:  # 빈 줄 제외
            data.append({
                '상품명': row['상품명'],
                '카테고리': row['카테고리'],
                '할인율': int(row['할인율']),
                '매출액': int(row['매출액'])
            })

# 할인율과 매출액 추출
discounts = [d['할인율'] for d in data]
revenues = [d['매출액'] for d in data]

# 기본 통계 계산
def mean(values):
    return sum(values) / len(values)

def std_dev(values):
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

# 피어슨 상관계수 계산
def correlation(x, y):
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)
    
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) * 
                           sum((y[i] - mean_y) ** 2 for i in range(n)))
    
    return numerator / denominator if denominator != 0 else 0

corr = correlation(discounts, revenues)

# 결과 출력
print("=" * 60)
print("할인율과 매출액 상관관계 분석 결과")
print("=" * 60)
print(f"\n데이터 개수: {len(data)}개")
print(f"\n할인율 통계:")
print(f"  평균: {mean(discounts):.1f}%")
print(f"  최소: {min(discounts)}%, 최대: {max(discounts)}%")
print(f"\n매출액 통계:")
print(f"  평균: {mean(revenues):,.0f}원")
print(f"  최소: {min(revenues):,}원, 최대: {max(revenues):,}원")
print(f"\n★ 상관계수: {corr:.4f}")

# 상관관계 해석
if abs(corr) < 0.3:
    strength = "약한"
elif abs(corr) < 0.7:
    strength = "중간 정도의"
else:
    strength = "강한"

direction = "양의" if corr > 0 else "음의"
print(f"   해석: {direction} {strength} 상관관계")

if corr > 0:
    print("   → 할인율이 높을수록 매출액이 증가하는 경향")
else:
    print("   → 할인율이 높을수록 매출액이 감소하는 경향")

# 할인율별 평균 매출 계산
discount_groups = {}
for d in data:
    disc = d['할인율']
    if disc not in discount_groups:
        discount_groups[disc] = []
    discount_groups[disc].append(d['매출액'])

print(f"\n할인율별 평균 매출액:")
for disc in sorted(discount_groups.keys()):
    avg = mean(discount_groups[disc])
    count = len(discount_groups[disc])
    print(f"  {disc:2d}% 할인: {avg:>10,.0f}원 ({count}개 상품)")

# 카테고리별 분석
categories = {}
for d in data:
    cat = d['카테고리']
    if cat not in categories:
        categories[cat] = {'discounts': [], 'revenues': []}
    categories[cat]['discounts'].append(d['할인율'])
    categories[cat]['revenues'].append(d['매출액'])

print(f"\n카테고리별 상관계수:")
for cat in sorted(categories.keys()):
    cat_corr = correlation(categories[cat]['discounts'], categories[cat]['revenues'])
    print(f"  {cat}: {cat_corr:6.3f}")

# HTML 시각화 생성
html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>할인율-매출액 상관관계 분석</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Malgun Gothic', sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 18px;
        }}
        .stats {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .stat-row {{
            display: flex;
            justify-content: space-around;
            text-align: center;
        }}
        .stat-box {{
            flex: 1;
            padding: 15px;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: #2196F3;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}
        @media (max-width: 768px) {{
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <h1>📊 할인율과 매출액 상관관계 분석</h1>
    <div class="subtitle">상관계수: <strong>{corr:.4f}</strong> ({direction} {strength} 상관관계)</div>
    
    <div class="stats">
        <div class="stat-row">
            <div class="stat-box">
                <div class="stat-value">{len(data)}</div>
                <div class="stat-label">전체 상품 수</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{mean(discounts):.1f}%</div>
                <div class="stat-label">평균 할인율</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{mean(revenues)/1000000:.1f}M</div>
                <div class="stat-label">평균 매출액 (백만원)</div>
            </div>
        </div>
    </div>

    <div class="chart-grid">
        <div class="chart-container">
            <canvas id="scatterChart"></canvas>
        </div>
        <div class="chart-container">
            <canvas id="barChart"></canvas>
        </div>
    </div>
    
    <div class="chart-container">
        <canvas id="categoryChart"></canvas>
    </div>

    <script>
        // 산점도 데이터
        const scatterData = {{
            datasets: [{{
                label: '상품별 데이터',
                data: {[[{'x': d['할인율'], 'y': d['매출액']} for d in data]]},
                backgroundColor: 'rgba(33, 150, 243, 0.6)',
                borderColor: 'rgba(33, 150, 243, 1)',
                borderWidth: 1,
                pointRadius: 6,
                pointHoverRadius: 8
            }}]
        }};

        // 산점도 차트
        new Chart(document.getElementById('scatterChart'), {{
            type: 'scatter',
            data: scatterData,
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: '할인율 vs 매출액 (산점도)',
                        font: {{ size: 16 }}
                    }},
                    legend: {{ display: false }}
                }},
                scales: {{
                    x: {{
                        title: {{ display: true, text: '할인율 (%)' }},
                        min: -5,
                        max: 55
                    }},
                    y: {{
                        title: {{ display: true, text: '매출액 (원)' }},
                        ticks: {{
                            callback: function(value) {{
                                return value.toLocaleString();
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // 할인율별 평균 매출
        const avgData = {dict((disc, mean(discount_groups[disc])) for disc in sorted(discount_groups.keys()))};
        
        new Chart(document.getElementById('barChart'), {{
            type: 'bar',
            data: {{
                labels: {list(sorted(discount_groups.keys()))},
                datasets: [{{
                    label: '평균 매출액',
                    data: {[mean(discount_groups[disc]) for disc in sorted(discount_groups.keys())]},
                    backgroundColor: 'rgba(76, 175, 80, 0.6)',
                    borderColor: 'rgba(76, 175, 80, 1)',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: '할인율별 평균 매출액',
                        font: {{ size: 16 }}
                    }}
                }},
                scales: {{
                    x: {{
                        title: {{ display: true, text: '할인율 (%)' }}
                    }},
                    y: {{
                        title: {{ display: true, text: '평균 매출액 (원)' }},
                        ticks: {{
                            callback: function(value) {{
                                return value.toLocaleString();
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // 카테고리별 상관계수
        const catCorr = {dict((cat, round(correlation(categories[cat]['discounts'], categories[cat]['revenues']), 3)) for cat in sorted(categories.keys()))};
        
        new Chart(document.getElementById('categoryChart'), {{
            type: 'bar',
            data: {{
                labels: {list(sorted(categories.keys()))},
                datasets: [{{
                    label: '상관계수',
                    data: {[round(correlation(categories[cat]['discounts'], categories[cat]['revenues']), 3) for cat in sorted(categories.keys())]},
                    backgroundColor: function(context) {{
                        const value = context.parsed.y;
                        return value >= 0 ? 'rgba(33, 150, 243, 0.6)' : 'rgba(244, 67, 54, 0.6)';
                    }},
                    borderColor: function(context) {{
                        const value = context.parsed.y;
                        return value >= 0 ? 'rgba(33, 150, 243, 1)' : 'rgba(244, 67, 54, 1)';
                    }},
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: '카테고리별 할인율-매출액 상관계수',
                        font: {{ size: 16 }}
                    }}
                }},
                scales: {{
                    x: {{
                        title: {{ display: true, text: '카테고리' }}
                    }},
                    y: {{
                        title: {{ display: true, text: '상관계수' }},
                        min: -1,
                        max: 1
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

# HTML 파일 저장
with open('discount_analysis.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n" + "=" * 60)
print("✓ 분석 완료!")
print("✓ 'discount_analysis.html' 파일이 생성되었습니다.")
print("  → 웹 브라우저로 열어서 시각화 결과를 확인하세요!")
print("=" * 60)

