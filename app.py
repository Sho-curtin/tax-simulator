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

st.title("日本税金シミュレーター（控除込み）")

income = st.number_input("年間所得（万円）", min_value=0, step=10)
asset = st.number_input("保有資産（万円）", min_value=0, step=100)
japan_resident = st.checkbox("日本に住所がある", value=True)

if st.button("税金を計算"):
    if japan_resident:
        income_tax = calc_income_tax(income)
        resident_tax = calc_resident_tax(income)
        total_tax = income_tax + resident_tax

        st.subheader("📊 税金の試算結果（基礎控除48万円適用）")
        st.write(f"所得税: {income_tax:.2f} 万円")
        st.write(f"住民税: {resident_tax:.2f} 万円")
        st.write(f"合計税額: {total_tax:.2f} 万円")
    else:
        st.info("非居住者の場合、日本では原則国内源泉所得のみが課税対象です。")
st.header("🌐 日豪相続モード切替シミュレーター")

mode = st.radio("相続税制度を選択", ["日本（Japan）", "オーストラリア（Australia）"])

if mode == "日本（Japan）":
    st.subheader("🇯🇵 日本モード")

    cash_asset = st.number_input("現金・預金の総額（万円）", min_value=0, step=100)
    property_value = st.number_input("不動産の評価額（万円）", min_value=0, step=100)
    total_inheritance = cash_asset + property_value

    num_children = st.number_input("子どもの人数", min_value=0, step=1)
    has_spouse = st.checkbox("配偶者がいる", value=True)

    heir_count = num_children + (1 if has_spouse else 0)
    basic_deduction = 3000 + 600 * heir_count
    taxable_inheritance = max(total_inheritance - basic_deduction, 0)
    share_per_heir = taxable_inheritance / heir_count if heir_count > 0 else 0

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

            st.write(f"📌 相続財産：{total_inheritance:.0f} 万円（うち不動産：{property_value:.0f} 万円）")
            st.write(f"基礎控除後：{taxable_inheritance:.0f} 万円")
            st.write(f"配偶者税額：{spouse_tax:.0f} 万円")
            st.write(f"子の税額合計：{child_tax_total:.0f} 万円")
            st.success(f"🇯🇵 相続税合計：{total_tax:.0f} 万円")

elif mode == "オーストラリア（Australia）":
    st.subheader("🇦🇺 オーストラリアモード")

    st.write("📝 オーストラリアには日本のような **相続税制度は存在しません。**")
    st.write("ただし、被相続人が亡くなった際に **キャピタルゲイン税（CGT）** が適用されることがあります。")
    st.write("CGTは資産を売却または相続人に引き継ぐときに、**値上がり益**に課税されます。")

    asset_value = st.number_input("譲渡される資産の評価額（AUD）", min_value=0, step=10000)
    cost_base = st.number_input("被相続人の取得価格（AUD）", min_value=0, step=10000)
    gain = max(asset_value - cost_base, 0)

    cgt_discount = st.checkbox("1年以上保有していた資産（50%控除）", value=True)

    if st.button("キャピタルゲイン税を試算"):
        taxable_gain = gain * (0.5 if cgt_discount else 1.0)
        cgt_tax = taxable_gain * 0.45  # 高所得層最大税率

        st.write(f"キャピタルゲイン：${gain:,.0f} AUD")
        st.write(f"課税対象利益：${taxable_gain:,.0f} AUD")
        st.success(f"推定CGT：${cgt_tax:,.0f} AUD（最大税率想定）")
