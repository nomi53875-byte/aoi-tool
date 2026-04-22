import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V6.8", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")

# 1. 檔案上傳
files = st.file_uploader("請【一次框選】多個檔案上傳", type=['aoi'], accept_multiple_files=True)

if files:
    st.info(f"📊 目前偵測到已上傳檔案數：{len(files)} 個")
    st.markdown("---")
    
    # 建立一個獨立的結果字典，確保資料不重疊
    all_final_data = {}

    # 第一階段：單純處理資料，不畫任何 UI
    for f in files:
        # 強制讀取檔案副本
        f.seek(0)
        raw_content = f.read().decode('gbk', errors='ignore')
        lines = raw_content.splitlines()
        
        output_rows = []
        seen = set()
        
        for line in lines:
            if not line.strip(): continue
            p = [i.strip() for i in line.split(',')]
            if len(p) < 6: continue
            
            try:
                # 抓取：座標符[0], X[3], Y[4], 角度[5], 料號[2]
                d, x, y, a, n = p[0], p[3], p[4], p[5], p[2]
                float(x); float(y)
            except:
                try:
                    # 備用格式
                    d, x, y, a, n = p[5], p[1], p[2], p[3], p[7]
                    float(x)
                except: continue

            if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                if d not in seen and "基准" not in line:
                    output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                    seen.add(d)

        if output_rows:
            target_name = os.path.splitext(f.name)[0] + ".txt"
            # 把結果存入字典，Key 是檔案名稱，Value 是轉換後的字串
            all_final_data[target_name] = "\r\n".join(output_rows)

    # 第二階段：當所有檔案都存進 all_final_data 後，才開始畫按鈕
    if all_final_data:
        st.markdown("### 📥 下載清單：")
        # 遍歷字典裡的每一個項目
        for fname, fdata in all_final_data.items():
            with st.expander(f"✅ 檔案就緒：{fname}", expanded=True):
                st.download_button(
                    label=f"📥 點我下載 {fname}",
                    data=fdata,
                    file_name=fname,
                    mime="text/plain",
                    # 用檔案名當作獨一無二的 Key
                    key=f"dl_key_{fname}"
                )
else:
    st.warning("請將檔案拖入上方區域。")
