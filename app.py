import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import openai
import os

st.set_page_config(page_title="日豪相続＆所得税シミュレーター", layout="centered")
st.title("🧾 日豪相続＆所得税シミュレーター")

# ---------------- 比較レポート ----------------
st.header("🔄 日本 vs オーストラリア 比較レポート")

with st.expander("📋 制度概要の比較表"):
    comparison_data = {
        "項目": ["相続税", "キャピタルゲイン税（資産売却時）", "基礎控除・免税枠", "税率構造", "申告義務"],
        "日本": [
            "あり（最高55%）",
            "一部あり（譲渡益課税）",
            "3000万円 + 600万円 × 法定相続人",
            "超過累進課税",
            "原則あり（10ヶ月以内）"
        ],
        "オーストラリア": [
            "なし（相続時点）",
            "あり（CGTベース）",
            "特別な免税枠なし（CGT割引あり）",
            "固定税率（45%など）",
            "売却時に申告"
        ]
    }
    df_compare = pd.DataFrame(comparison_data)
    st.dataframe(df_compare, use_container_width=True)

# ---------------- 所得税・住民税シミュレーター ----------------
st.header("💰 所得税・住民税シミュレーター（日本）")

income = st.number_input("年間所得額（万円）", min_value=0, step=50)
basic_deduction = 48  # 万円（基礎控除）
taxable_income = max(income - basic_deduction, 0)

# 所得税率（簡易版）
income_tax_brackets = [195, 330, 695, 900, 1800, float("inf")]
income_tax_rates = [0.05, 0.10, 0.20, 0.23, 0.33, 0.40]
income_tax_deductions = [0, 9.75, 42.75, 63.6, 153.6, 279.6]

def calc_income_tax(amount):
    for i, threshold in enumerate(income_tax_brackets):
        if amount <= threshold:
            return max(amount * income_tax_rates[i] - income_tax_deductions[i], 0)
    return 0

income_tax = calc_income_tax(taxable_income)
resident_tax = taxable_income * 0.10

if st.button("所得税＋住民税を計算する"):
    st.subheader("📊 税額の試算結果")
    st.write(f"課税所得額：{taxable_income:.1f} 万円")
    st.write(f"所得税：{income_tax:.1f} 万円")
    st.write(f"住民税：{resident_tax:.1f} 万円")
    st.success(f"合計納税額：約 {income_tax + resident_tax:.1f} 万円")

# ---------------- 不動産情報入力 ----------------
st.header("🏠 不動産情報")

with st.expander("📦 不動産評価額の入力"):
    land_value = st.number_input("土地の評価額（万円）", min_value=0, step=100)
    building_value = st.number_input("建物の評価額（万円）", min_value=0, step=100)
    location = st.text_input("所在地（例：東京都港区）")
    total_property_value = land_value + building_value

    if total_property_value > 0:
        st.write(f"🧾 総不動産価値：{total_property_value} 万円")

# ---------------- 相続税シミュレーター ----------------
st.header("🏡 相続税簡易シミュレーター（日本）")

total_cash = st.number_input("現金・預金（万円）", min_value=0, step=100)
total_stocks = st.number_input("株・ETF・投資信託（万円）", min_value=0, step=100)
total_others = st.number_input("その他資産（万円）", min_value=0, step=100)
total_assets = total_cash + total_stocks + total_others + total_property_value

num_heirs = st.number_input("法定相続人の数（人）", min_value=1, step=1)
exemption_base = 3000 + 600 * num_heirs

if st.button("相続税を簡易計算"):
    taxable_inherit = max(total_assets - exemption_base, 0)
    est_inherit_tax = taxable_inherit * 0.20  # 仮に20%で試算
    st.subheader("🧮 相続税の試算結果")
    st.write(f"総資産額：{total_assets:.1f} 万円")
    st.write(f"基礎控除額：{exemption_base:.1f} 万円")
    st.write(f"課税対象額：{taxable_inherit:.1f} 万円")
    st.success(f"推定相続税：約 {est_inherit_tax:.1f} 万円（20%想定）")

# ---------------- AIアドバイザー ----------------
st.header("🤖 AI相続・税金アドバイザー（ChatGPT風）")

openai_api_key = st.text_input("OpenAI APIキーを入力", type="password")
question = st.text_area("ご相談内容を入力（例：相続税を抑えるには？）")

if st.button("AIに相談する") and openai_api_key and question:
    try:
        openai.api_key = openai_api_key
        with st.spinner("AIが回答中..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは日本とオーストラリアの税制・相続制度に詳しい専門家です。"},
                    {"role": "user", "content": question}
                ]
            )
            answer = response["choices"][0]["message"]["content"]
            st.success("AIの回答：")
            st.write(answer)
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
elif st.button("AIに相談する"):
    st.warning("APIキーと相談内容を入力してください。")

# ---------------- 法改正アップデート案内 ----------------
st.info("📚 このシミュレーターは令和6年度日本税制・2024年豪州CGT制度に基づいています。アップデートが必要な場合は最新の法改正をご確認ください。GitHub: https://github.com/yourrepo")
