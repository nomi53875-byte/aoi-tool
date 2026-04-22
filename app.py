import os

# 自動檢查並安裝必要的零件，這能解決 222.jpg 看到的錯誤
try:
    import streamlit as st
    import pandas as pd
except ImportError:
    os.system("pip install streamlit pandas")
    import streamlit as st
    import pandas as pd

# 設定網頁標題
st.set_page_config(page_title="SMT 工具 V5.0", layout="centered")

st.title("🚀 SMT AOI 萬用轉檔工具")
st.success("✅ 版本 V5.0：純淨下載模式已啟動，下方絕無清單。")

uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        output_rows = []
        seen = set()
        
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) >= 6:
                try:
                    # 格式 A
                    d, x, y, a, n = parts[0].strip(), parts[3].strip(), parts[4].strip(), parts[5].strip(), parts[2].strip()
                    float(x), float(y)
                except:
                    try:
                        # 格式 B
                        d, x, y, a, n = parts[5].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[7].strip()
                        float(x), float(y)
                    except: continue

                # 排除標題列與重複項
                if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                    if d not in seen and "基准" not in line:
                        output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                        seen.add(d)

        if output_rows:
            result = "\n".join(output_rows)
            st.download_button(
                label="📥 點我下載轉檔後的座標檔 (.txt)",
                data=result,
                file_name="SMT_Coordinate_Fixed.txt",
                mime="text/plain"
            )
            st.info(f"💡 處理完成！共轉換 {len(output_rows)} 筆座標。")
    except Exception as e:
        st.error(f"發生錯誤：{e}")
