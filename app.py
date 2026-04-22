import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V6.6", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")

# 1. 檔案上傳
uploaded_files = st.file_uploader("請【框選】多個檔案上傳", type=['aoi'], accept_multiple_files=True)

if uploaded_files:
    st.info(f"📊 目前偵測到已上傳檔案數：{len(uploaded_files)} 個")
    st.markdown("---")
    
    # 建立一個容器來一次顯示所有按鈕
    results_to_show = []

    for index, uploaded_file in enumerate(uploaded_files):
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
                # 將處理好的資料存入暫存清單
                results_to_show.append({
                    "filename": output_filename,
                    "data": final_result,
                    "key": f"btn_v66_{index}_{base_name}"
                })
            
            # 讀取完畢歸零
            uploaded_file.seek(0)
                    
        except Exception as e:
            st.error(f"檔案 {uploaded_file.name} 處理出錯: {e}")

    # 2. 統一在最後把清單畫出來
    if results_to_show:
        st.markdown("### 📥 下載清單：")
        for item in results_to_show:
            with st.expander(f"✅ 檔案就緒：{item['filename']}", expanded=True):
                st.download_button(
                    label=f"📥 下載 {item['filename']}",
                    data=item['data'],
                    file_name=item['filename'],
                    mime="text/plain",
                    key=item['key']
                )
else:
    st.warning("請將檔案拖入上方區域。")
