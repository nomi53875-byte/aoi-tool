import streamlit as st
import pandas as pd

# 強制設定網頁標題與風格
st.set_page_config(page_title="SMT 工具 V5.0", layout="centered")

st.title("🚀 SMT AOI 萬用轉檔工具")
st.markdown("---")
st.success("✅ 版本 V5.0：純淨下載模式（格式與檔名已修正）")

# 檔案上傳器
uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        # 讀取檔案內容
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        
        output_rows = []
        seen_designators = set()
        
        for line in lines:
            if not line.strip():
                continue
            
            parts = [p.strip() for p in line.split(',')]
            
            # 初始化變數
            d, x, y, a, n = "", "", "", "", ""
            
            try:
                # 嘗試格式 A (常見格式)
                if len(parts) >= 6:
                    d, x, y, a, n = parts[0], parts[3], parts[4], parts[5], parts[2]
                    float(x), float(y) # 驗證座標是否為數字
                else:
                    raise ValueError
            except:
                try:
                    # 嘗試格式 B (備用格式)
                    if len(parts) >= 8:
                        d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                        float(x), float(y)
                except:
                    continue # 格式不符就跳過

            # 過濾條件：排除標題、重複項、基準點
            if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                if d not in seen_designators and "基准" not in line:
                    # 嚴格執行 座標符 [TAB] X [TAB] Y [TAB] 角度 [TAB] T [TAB] 料號
                    output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                    seen_designators.add(d)

        if output_rows:
            # 組合最終文字內容
            final_result = "\n".join(output_rows)
            
            # 下載按鈕，設定正確的檔名
            st.download_button(
                label="📥 點我下載轉檔後的座標檔 (.txt)",
                data=final_result,
                file_name="Converted_Coordinate.txt",
                mime="text/plain"
            )
            st.info(f"💡 轉換成功！總計：{len(output_rows)} 筆數據。")
            
    except Exception as e:
        st.error(f"轉換過程中發生錯誤：{e}")

st.markdown("---")
st.caption("提示：若網頁無法開啟，請確認 GitHub 專案中是否有 requirements.txt 檔案。")
