import streamlit as st
import os

# 設定網頁標題
st.set_page_config(page_title="SMT 工具 V5.4", layout="centered")

st.title("🚀 SMT AOI 萬用轉檔工具")
st.success("✅ 版本 V5.4：換行格式與檔名最終修正")

uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        # 1. 取得原始檔名並將副檔名改為 .txt
        base_name = os.path.splitext(uploaded_file.name)[0]
        output_filename = f"{base_name}.txt"

        # 2. 讀取原始檔案內容
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        
        output_rows = []
        seen = set()
        
        for line in lines:
            if not line.strip(): continue
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) < 6: continue
            
            d, x, y, a, n = "", "", "", "", ""
            
            try:
                # 根據標準格式 BNG012-010YFA.txt 對齊欄位
                # parts[0]=座標符, parts[3]=X, parts[4]=Y, parts[5]=角度, parts[2]=料號
                d, x, y, a, n = parts[0], parts[3], parts[4], parts[5], parts[2]
                float(x); float(y) # 數字驗證
            except:
                try:
                    # 備用抓取邏輯
                    d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                    float(x)
                except:
                    continue

            # 過濾標題與重複項
            if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                if d not in seen and "基准" not in line:
                    # 使用 Tab 鍵 (\t) 對齊
                    output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                    seen.add(d)

        if output_rows:
            # 3. 關鍵修正：使用 \r\n 確保在 Windows/SMT 系統中正確換行
            final_result = "\r\n".join(output_rows)
            
            st.info(f"準備輸出檔案：{output_filename}")
            
            # 4. 提供下載
            st.download_button(
                label=f"📥 點我下載 {output_filename}",
                data=final_result,
                file_name=output_filename,
                mime="text/plain"
            )
            st.success(f"💡 轉換成功！總計 {len(output_rows)} 筆。")
            
    except Exception as e:
        st.error(f"發生錯誤：{e}")
