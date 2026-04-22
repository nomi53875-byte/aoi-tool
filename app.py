import streamlit as st
import os
import io
import zipfile

# 設定網頁標題
st.set_page_config(page_title="SMT 批量轉檔工具 V6.0", layout="centered")

st.title("📦 SMT AOI 批量自動化轉換系統")
st.success("✅ 版本 V6.0：支援多檔案拖曳 + 自動打包 ZIP 下載")

# 1. 關鍵改動：accept_multiple_files=True 允許一次選取多個檔案
uploaded_files = st.file_uploader("請拖曳多個 AOI 檔案進去", type=['aoi'], accept_multiple_files=True)

if uploaded_files:
    # 建立一個記憶體緩存來存放 ZIP 檔案
    zip_buffer = io.BytesIO()
    
    # 準備建立壓縮檔
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        count = 0
        
        for uploaded_file in uploaded_files:
            try:
                # 取得檔名並轉換為 .txt
                base_name = os.path.splitext(uploaded_file.name)[0]
                output_filename = f"{base_name}.txt"

                # 讀取內容
                content = uploaded_file.read().decode('gbk', errors='ignore')
                lines = content.splitlines()
                output_rows = []
                seen = set()

                for line in lines:
                    if not line.strip(): continue
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) < 6: continue
                    
                    try:
                        # 核心格式抓取 (座標符, X, Y, 角度, 料號)
                        d, x, y, a, n = parts[0], parts[3], parts[4], parts[5], parts[2]
                        float(x); float(y)
                    except:
                        try:
                            d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                            float(x)
                        except: continue

                    if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                        if d not in seen and "基准" not in line:
                            output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)

                if output_rows:
                    # 組合文字內容並使用 \r\n 換行
                    final_text = "\r\n".join(output_rows)
                    # 將結果寫入 ZIP 壓縮包中
                    zip_file.writestr(output_filename, final_text)
                    count += 1
            except Exception as e:
                st.error(f"檔案 {uploaded_file.name} 轉換失敗: {e}")

        # 如果有成功轉換的檔案
        if count > 0:
            st.markdown(f"---")
            st.info(f"🎉 已成功處理 **{count}** 個檔案！")
            
            # 提供 ZIP 下載按鈕
            st.download_button(
                label="📥 點我一口氣下載所有 TXT (ZIP檔)",
                data=zip_buffer.getvalue(),
                file_name="SMT_Converted_Files.zip",
                mime="application/zip"
            )
