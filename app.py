import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V6.9", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")

# 1. 檔案上傳 (使用新的標籤)
all_files = st.file_uploader("請一次選取多個檔案", type=['aoi'], accept_multiple_files=True, key="smt_uploader")

if all_files:
    # 建立一個獨立的資料盒
    processed_data = {}

    # 第一步：把所有檔案先處理好存進「資料盒」
    for f in all_files:
        # 強制讀取並解碼
        try:
            f.seek(0)
            raw = f.read().decode('gbk', errors='ignore')
            lines = raw.splitlines()
            
            output = []
            seen = set()
            for line in lines:
                if not line.strip(): continue
                p = [i.strip() for i in line.split(',')]
                if len(p) < 6: continue
                try:
                    # 抓取：座標符, X, Y, 角度, 料號
                    d, x, y, a, n = p[0], p[3], p[4], p[5], p[2]
                    float(x); float(y)
                    if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                        if d not in seen and "基准" not in line:
                            output.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)
                except: continue
            
            if output:
                # 檔名作為 Key，轉換後的內容作為 Value
                file_id = os.path.splitext(f.name)[0] + ".txt"
                processed_data[file_id] = "\r\n".join(output)
        except Exception as e:
            st.error(f"檔案 {f.name} 處理失敗")

    # 第二步：根據資料盒的內容，一個一個畫出按鈕
    if processed_data:
        st.info(f"📊 系統已確認處理完成 {len(processed_data)} 個檔案")
        st.markdown("---")
        
        # 這裡用一個表格列出清單，確保每個檔案都有位置
        for name, content in processed_data.items():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"📄 **{name}**")
                with col2:
                    st.download_button(
                        label="📥 下載",
                        data=content,
                        file_name=name,
                        mime="text/plain",
                        key=f"dl_btn_{name}" # 用檔名當唯一 ID
                    )
                st.markdown("---")
else:
    st.warning("請選取檔案上傳。")
