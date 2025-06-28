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
