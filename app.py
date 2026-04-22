import streamlit as st
import os

# 設定網頁標題
st.set_page_config(page_title="SMT 批量合併工具 V6.1", layout="centered")

st.title("📋 SMT 批量合併轉檔系統")
st.success("✅ 版本 V6.1：多檔案拖曳 + 自動合併為單一 TXT (免解壓)")

# 支援多檔案選取
uploaded_files = st.file_uploader("請拖曳多個 AOI 檔案進去", type=['aoi'], accept_multiple_files=True)

if uploaded_files:
    combined_result = ""
    file_count = 0
    total_rows = 0

    for uploaded_file in uploaded_files:
        try:
            # 讀取原始檔名作為區隔標籤
            file_name_label = os.path.splitext(uploaded_file.name)[0]
            
            # 讀取內容 (GBK 編碼)
            content = uploaded_file.read().decode('gbk', errors='ignore')
            lines = content.splitlines()
            
            current_file_rows = []
            seen = set()

            for line in lines:
                if not line.strip(): continue
                parts = [p.strip() for p in line.split(',')]
                if len(parts) < 6: continue
                
                try:
                    # 格式抓取
                    d, x, y, a, n = parts[0], parts[3], parts[4], parts[5], parts[2]
                    float(x); float(y)
                except:
                    try:
                        d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                        float(x)
                    except: continue

                if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                    if d not in seen and "基准" not in line:
                        current_file_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                        seen.add(d)

            if current_file_rows:
                # 在合併的內容中加入檔案標籤，方便現場區分
                combined_result += f"--- 檔案: {file_name_label} ---\r\n"
                combined_result += "\r\n".join(current_file_rows) + "\r\n\r\n"
                file_count += 1
                total_rows += len(current_file_rows)
                
        except Exception as e:
            st.error(f"檔案 {uploaded_file.name} 轉換失敗: {e}")

    if file_count > 0:
        st.markdown(f"---")
        st.info(f"📊 已完成合併：共 **{file_count}** 個專案，合計 **{total_rows}** 筆座標。")
        
        # 產生下載按鈕，檔名預設為合併後的名稱
        st.download_button(
            label="📥 點我下載合併後的座標檔 (Combined_Coordinate.txt)",
            data=combined_result,
            file_name="Combined_Coordinate.txt",
            mime="text/plain"
        )
