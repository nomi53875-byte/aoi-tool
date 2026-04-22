import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V6.4", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")

# 1. 這裡加入一個明顯的計數器提示
uploaded_files = st.file_uploader("請【框選】或【按住Ctrl選取】多個檔案", type=['aoi'], accept_multiple_files=True)

if uploaded_files:
    # 顯示目前抓到的檔案數量，這能幫我們確認上傳是否成功
    st.info(f"📊 目前偵測到已上傳檔案數：{len(uploaded_files)} 個")
    st.markdown("---")
    st.markdown("### 📥 下載清單：")

    # 2. 核心處理邏輯
    for uploaded_file in uploaded_files:
        try:
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
                final_result = "\r\n".join(output_rows)
                
                # 3. 使用排版容器，確保每個檔案都有自己的區塊
                with st.expander(f"✅ 檔案就緒：{output_filename}", expanded=True):
                    st.download_button(
                        label=f"📥 點我下載 {output_filename}",
                        data=final_result,
                        file_name=output_filename,
                        mime="text/plain",
                        key=f"btn_{output_filename}_{len(output_rows)}" # 加入動態 key 避免衝突
                    )
                    
        except Exception as e:
            st.error(f"檔案 {uploaded_file.name} 處理出錯: {e}")

else:
    st.warning("目前尚未選取檔案，請將檔案拖入上方區域。")
