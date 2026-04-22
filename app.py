import streamlit as st
import os

# 設定網頁標題
st.set_page_config(page_title="SMT 工具 V5.5", layout="centered")

st.title("📊 座標自動化轉換")
st.success("✅ 版本 V5.5：終極完美版 (檔名與換行全修正)")

uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        # 1. 動態抓取原始檔名並改為 .txt
        base_name = os.path.splitext(uploaded_file.name)[0]
        output_filename = f"{base_name}.txt"

        # 2. 讀取原始內容 (GBK 編碼)
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        
        output_rows = []
        seen = set()
        
        for line in lines:
            if not line.strip(): continue
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) < 6: continue
            
            try:
                # 對應標準格式抓取欄位
                # d=座標符[0], x=X[3], y=Y[4], a=角度[5], n=料號[2]
                d, x, y, a, n = parts[0], parts[3], parts[4], parts[5], parts[2]
                float(x); float(y) # 驗證座標是否為數字
            except:
                try:
                    # 備用格式抓取
                    d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                    float(x)
                except:
                    continue

            # 過濾標題、基準點與重複座標
            if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                if d not in seen and "基准" not in line:
                    # 使用 \t (Tab) 進行欄位對齊
                    output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                    seen.add(d)

        if output_rows:
            # 3. 關鍵修正：使用 \r\n 確保在所有系統都能正確換行
            final_result = "\r\n".join(output_rows)
            
            # 4. 提供與原始檔案同名的下載按鈕
            st.download_button(
                label=f"📥 點我下載 {output_filename}",
                data=final_result,
                file_name=output_filename,
                mime="text/plain"
            )
            st.info(f"💡 完美達成！轉換檔案：{output_filename}，總計 {len(output_rows)} 筆。")
            
    except Exception as e:
        st.error(f"發生錯誤：{e}")
