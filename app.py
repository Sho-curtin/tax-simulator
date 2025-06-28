import streamlit as st

def calc_income_tax(income):
    taxable = max(income - 48, 0)  # 万円単位、基礎控除48万円
    brackets = [195, 330, 695, 900, 1800, 4000]
    rates = [0.05, 0.10, 0.20, 0.23, 0.33, 0.40, 0.45]
    deductions = [0, 9.75, 42.75, 63.6, 153.6, 279.6, 479.6]

    for i, threshold in enumerate(brackets):
        if taxable <= threshold:
            return max(taxable * rates[i] - deductions[i], 0)
    return max(taxable * rates[-1] - deductions[-1], 0)

def calc_resident_tax(income):
    taxable = max(income - 48, 0)
    return taxable * 0.10

import streamlit as st

st.set_page_config(page_title="日豪相続シミュレーター", layout="centered")
st.title("🌏 日豪相続シミュレーター")

mode = st.radio("相続税制度を選択してください", ["日本（Japan）", "オーストラリア（Australia）"])

if mode == "日本（Japan）":
    st.subheader("🇯🇵 日本モード")

    st.markdown("### 💰 資産内容の入力")
    cash_asset = st.number_input("現金・預金（万円）", min_value=0, step=100)
    property_value = st.number_input("不動産評価額（万円）", min_value=0, step=100)
    stock_value = st.number_input("上場株式（万円）", min_value=0, step=100)
    etf_value = st.number_input("ETF（万円）", min_value=0, step=100)
    fund_value = st.number_input("投資信託（万円）", min_value=0, step=100)

    total_inheritance = cash_asset + property_value + stock_value + etf_value + fund_value

    st.markdown("### 👪 家族構成")
    num_children = st.number_input("子どもの人数", min_value=0, step=1)
    has_spouse = st.checkbox("配偶者がいる", value=True)

    heir_count = num_children + (1 if has_spouse else 0)
    basic_deduction = 3000 + 600 * heir_count
    taxable_inheritance = max(total_inheritance - basic_deduction, 0)
    share_per_heir = taxable_inheritance / heir_count if heir_count > 0 else 0

    # 相続税計算ロジック
    brackets = [1000, 3000, 5000, 10000, 20000, float("inf")]
    rates = [0.10, 0.15, 0.20, 0.30, 0.40, 0.55]
    deductions = [0, 50, 200, 700, 1700, 0]

    def calc_tax(amount):
        for i, threshold in enumerate(brackets):
            if amount <= threshold:
                return max(amount * rates[i] - deductions[i], 0)
        return 0

    if st.button("日本モードで相続税を計算"):
        if heir_count == 0:
            st.warning("相続人がいない場合は計算できません。")
        else:
            spouse_tax = 0
            child_tax_total = 0

            if has_spouse:
                spouse_share = share_per_heir
                spouse_exempt = min(16000, spouse_share)
                spouse_tax = calc_tax(spouse_share - spouse_exempt)

            for _ in range(int(num_children)):
                child_tax_total += calc_tax(share_per_heir)

            total_tax = spouse_tax + child_tax_total

            st.markdown("### 📦 相続財産の内訳")
            st.write(f"- 現金・預金：{cash_asset:.0f} 万円")
            st.write(f"- 不動産：{property_value:.0f} 万円")
            st.write(f"- 上場株式：{stock_value:.0f} 万円")
            st.write(f"- ETF：{etf_value:.0f} 万円")
            st.write(f"- 投資信託：{fund_value:.0f} 万円")

            st.markdown("### 📊 試算結果")
            st.write(f"総遺産額：{total_inheritance:.0f} 万円")
            st.write(f"基礎控除額：{basic_deduction:.0f} 万円")
            st.write(f"課税遺産額：{taxable_inheritance:.0f} 万円")
            st.write(f"配偶者の税額：{spouse_tax:.0f} 万円")
            st.write(f"子の税額合計：{child_tax_total:.0f} 万円")
            st.success(f"🇯🇵 相続税合計：{total_tax:.0f} 万円")

else:
    st.subheader("🇦🇺 オーストラリアモード")

    st.markdown("### 💡 オーストラリアは原則 **相続税なし** です。")
    st.write("- ただしキャピタルゲイン税（CGT）が発生することがあります。")
    st.write("- 相続人が資産を売却する際、取得時との差額に税金がかかる可能性があります。")

    asset_value = st.number_input("譲渡資産の現在の評価額（AUD）", min_value=0, step=10000)
    cost_base = st.number_input("取得価格（Cost Base）（AUD）", min_value=0, step=10000)
    gain = max(asset_value - cost_base, 0)

    cgt_discount = st.checkbox("1年以上保有していた（50%控除適用）", value=True)

    if st.button("CGT（キャピタルゲイン税）を計算"):
        taxable_gain = gain * (0.5 if cgt_discount else 1.0)
        cgt_tax = taxable_gain * 0.45  # 上位税率
        st.write(f"キャピタルゲイン：${gain:,.0f} AUD")
        st.write(f"課税対象額（控除後）：${taxable_gain:,.0f} AUD")
        st.success(f"🇦🇺 想定されるCGT：${cgt_tax:,.0f} AUD")
