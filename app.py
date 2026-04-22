import streamlit as st
import os
import time

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V6.5", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")

# 1. 檔案上傳
uploaded_files = st.file_uploader("請【框選】多個檔案上傳", type=['aoi'], accept_multiple_files=True)

if uploaded_files:
    st.info(f"📊 目前偵測到已上傳檔案數：{len(uploaded_files)} 個")
    st.markdown("---")
    st.markdown("### 📥 下載清單：")

    # 使用清單來存放處理好的資料，避免迴圈內衝突
    for index, uploaded_file in enumerate(uploaded_files):
        try:
            # 取得檔名
            base_name = os.path.splitext(uploaded_file.name)[0]
            output_filename = f"{base_name}.txt"

            # 讀取並處理內容
            content = uploaded_file.read().decode('gbk', errors='ignore')
            lines = content.splitlines()
            output_rows = []
            seen = set()
            
            for line in lines:
                if not line.strip(): continue
                parts = [p.strip() for p in line.split(',')]
                if len(parts) < 6: continue
                
                try:
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

            # 2. 關鍵修復：確保每個檔案都有獨立的區塊與唯一的 Key
            if output_rows:
                final_result = "\r\n".join(output_rows)
                
                # 使用 index (0, 1, 2...) 來確保每個按鈕的身分證字號完全不同
                with st.expander(f"✅ 檔案就緒：{output_filename}", expanded=True):
                    st.download_button(
                        label=f"📥 下載 {output_filename}",
                        data=final_result,
                        file_name=output_filename,
                        mime="text/plain",
                        key=f"btn_{index}_{base_name}" 
                    )
            
            # 讀取完後重設檔案指標，避免重複讀取錯誤
            uploaded_file.seek(0)
                    
        except Exception as e:
            st.error(f"檔案 {uploaded_file.name} 處理出錯: {e}")

else:
    st.warning("請將檔案拖入上方區域。")
