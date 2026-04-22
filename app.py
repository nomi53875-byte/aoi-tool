import streamlit as st
import os

# 設定網頁標題
st.set_page_config(page_title="SMT 批量轉檔工具 V6.2", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.success("✅ 版本 V6.2：支援多檔案拖曳 + 獨立下載按鈕 (免解壓)")

# 允許多檔案上傳
uploaded_files = st.file_uploader("請拖曳多個 AOI 檔案進去", type=['aoi'], accept_multiple_files=True)

if uploaded_files:
    st.markdown("### 📥 轉換完成，請分別點擊下載：")
    
    for uploaded_file in uploaded_files:
        try:
            # 1. 自動抓取原始檔名並改為 .txt
            base_name = os.path.splitext(uploaded_file.name)[0]
            output_filename = f"{base_name}.txt"

            # 2. 讀取內容 (GBK 編碼)
            content = uploaded_file.read().decode('gbk', errors='ignore')
            lines = content.splitlines()
            
            output_rows = []
            seen = set()
            
            for line in lines:
                if not line.strip(): continue
                parts = [p.strip() for p in line.split(',')]
                
                if len(parts) < 6: continue
                
                try:
                    # 抓取座標符[0], X[3], Y[4], 角度[5], 料號[2]
                    d, x, y, a, n = parts[0], parts[3], parts[4], parts[5], parts[2]
                    float(x); float(y) 
                except:
                    try:
                        # 備用抓取邏輯
                        d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                        float(x)
                    except: continue

                if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                    if d not in seen and "基准" not in line:
                        # Tab 鍵對齊
                        output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                        seen.add(d)

            if output_rows:
                # 3. 組合文字 (Windows 換行格式)
                final_result = "\r\n".join(output_rows)
                
                # 4. 為每個檔案生成獨立的下載按鈕
                # 用 columns 讓介面整齊一點
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"📄 {output_filename}")
                with col2:
                    st.download_button(
                        label="下載",
                        data=final_result,
                        file_name=output_filename,
                        mime="text/plain",
                        key=f"btn_{output_filename}" # 給每個按鈕唯一識別碼
                    )
                st.markdown("---")
                
        except Exception as e:
            st.error(f"檔案 {uploaded_file.name} 處理出錯: {e}")
