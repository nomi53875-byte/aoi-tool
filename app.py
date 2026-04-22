import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V7.1", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.success("✅ 版本 V7.1：支援大小寫副檔名 ( .aoi / .AOI )")

# 1. 初始化狀態
if 'file_results' not in st.session_state:
    st.session_state['file_results'] = {}

# 2. 檔案上傳：將 type 改成包含大寫
uploaded_files = st.file_uploader("請【一次框選】多個檔案上傳", type=['aoi', 'AOI'], accept_multiple_files=True)

if uploaded_files:
    # 每次重新上傳時清空舊資料
    st.session_state['file_results'] = {}
    
    for f in uploaded_files:
        try:
            # 讀取內容
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
                    # 座標符[0], X[3], Y[4], 角度[5], 料號[2]
                    d, x, y, a, n = p[0], p[3], p[4], p[5], p[2]
                    float(x); float(y)
                    if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                        if d not in seen and "基准" not in line:
                            output.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)
                except: continue
            
            if output:
                # 檔名處理：不論原始大小寫，輸出統一給 .txt
                fname = os.path.splitext(f.name)[0] + ".txt"
                st.session_state['file_results'][fname] = "\r\n".join(output)
        except Exception as e:
            st.error(f"檔案 {f.name} 處理失敗")

# 3. 顯示結果
if st.session_state['file_results']:
    count = len(st.session_state['file_results'])
    st.info(f"📊 成功辨識並處理 {count} 個檔案")
    st.markdown("---")
    
    for name in sorted(st.session_state['file_results'].keys()):
        with st.container():
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"📄 **{name}**")
            with c2:
                st.download_button(
                    label="📥 下載",
                    data=st.session_state['file_results'][name],
                    file_name=name,
                    mime="text/plain",
                    key=f"final_v71_{name}"
                )
            st.markdown("---")
