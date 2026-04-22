import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V6.7", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")

# 1. 檔案上傳
uploaded_files = st.file_uploader("請【一次框選】多個檔案上傳", type=['aoi'], accept_multiple_files=True)

if uploaded_files:
    st.info(f"📊 目前偵測到已上傳檔案數：{len(uploaded_files)} 個")
    st.markdown("---")
    st.markdown("### 📥 下載清單：")

    # 建立一個清單來存放所有處理完的資料
    # 使用 Python 的 List 來確保順序和內容不會被覆蓋
    final_output_list = []

    for uploaded_file in uploaded_files:
        try:
            # 取得原始檔名
            base_name = os.path.splitext(uploaded_file.name)[0]
            output_filename = f"{base_name}.txt"

            # 關鍵修正：每次讀取都先強制歸零，並讀取成一份獨立的副本
            uploaded_file.seek(0)
            raw_data = uploaded_file.read()
            
            # 使用 GBK 解碼
            content = raw_data.decode('gbk', errors='ignore')
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
                        # 備用格式
                        d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                        float(x)
                    except: continue

                if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                    if d not in seen and "基准" not in line:
                        output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                        seen.add(d)

            if output_rows:
                # 存入清單，這裡用 \r\n 換行
                final_output_list.append({
                    "name": output_filename,
                    "content": "\r\n".join(output_rows)
                })
                    
        except Exception as e:
            st.error(f"檔案 {uploaded_file.name} 處理出錯: {e}")

    # 2. 核心改動：等所有檔案都處理進 List 後，再統一印出按鈕
    if final_output_list:
        for idx, item in enumerate(final_output_list):
            # 使用獨一無二的 key (序號 + 檔名) 避免按鈕衝突
            with st.expander(f"✅ 檔案就緒：{item['name']}", expanded=True):
                st.download_button(
                    label=f"📥 點我下載 {item['name']}",
                    data=item['content'],
                    file_name=item['name'],
                    mime="text/plain",
                    key=f"final_dl_{idx}_{item['name']}"
                )
else:
    st.warning("請將檔案拖入上方區域。")
