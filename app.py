import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V7.2", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.success("✅ 版本 V7.2：解決大小寫混合上傳遺失問題")

# 1. 狀態初始化
if 'data_box' not in st.session_state:
    st.session_state['data_box'] = {}

# 2. 檔案上傳：手動列出所有可能的大小寫組合，確保 UI 接收
files = st.file_uploader("請選取多個檔案 (支援 .aoi / .AOI)", type=['aoi', 'AOI', 'Aoi'], accept_multiple_files=True)

if files:
    # 只要有新上傳，就清空舊狀態重新裝載
    st.session_state['data_box'] = {}
    
    for f in files:
        try:
            # 強制歸零讀取
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
                    d, x, y, a, n = p[0], p[3], p[4], p[5], p[2]
                    float(x); float(y)
                    if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                        if d not in seen and "基准" not in line:
                            output.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)
                except: continue
            
            if output:
                # 這裡最關鍵：不管原始檔名是 .AOI 還是 .aoi，統一產出 .txt
                # 使用檔案物件的名稱作為唯一 Key
                fname = os.path.splitext(f.name)[0] + ".txt"
                st.session_state['data_box'][f.name] = {
                    "output_name": fname,
                    "content": "\r\n".join(output)
                }
        except Exception as e:
            st.error(f"檔案 {f.name} 處理出錯")

# 3. 顯示結果
if st.session_state['data_box']:
    st.info(f"📊 偵測到 {len(files)} 個檔案，成功轉換 {len(st.session_state['data_box'])} 個項目")
    st.markdown("---")
    
    # 遍歷資料盒內容
    for original_name, info in st.session_state['data_box'].items():
        with st.container():
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"📄 **{info['output_name']}**")
                st.caption(f"原始檔名: {original_name}")
            with c2:
                st.download_button(
                    label="📥 下載",
                    data=info['content'],
                    file_name=info['output_name'],
                    mime="text/plain",
                    key=f"v72_{original_name}" # 使用原始檔名當 Key 絕對不重複
                )
            st.markdown("---")
