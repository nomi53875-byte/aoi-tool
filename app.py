import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V7.4", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.info("✅ 版本 V7.4：Debug 強制顯影模式")

# 1. 萬用上傳：完全不設 type，讓所有檔案都能進來
files = st.file_uploader("請【一次選取】多個檔案上傳", accept_multiple_files=True, key="debug_uploader")

if files:
    # 顯示 Debug 資訊：讓你知道系統「實際上」收到了哪些檔名
    st.write("---")
    st.write(f"🔍 **系統偵測到以下檔案 (共 {len(files)} 個)：**")
    for f in files:
        st.write(f"- `{f.name}` (大小: {f.size} bytes)")
    st.write("---")

    # 建立一個暫存空間
    if 'data_center' not in st.session_state:
        st.session_state['data_center'] = {}
    
    # 清空舊資料
    st.session_state['data_center'] = {}

    for f in files:
        try:
            # 只要是檔案就讀取內容，不預設副檔名
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
                new_name = os.path.splitext(f.name)[0] + ".txt"
                st.session_state['data_center'][f.name] = {
                    "output_name": new_name,
                    "content": "\r\n".join(output)
                }
        except Exception as e:
            st.write(f"❌ 檔案 {f.name} 內部格式解析失敗: {e}")

    # 顯示下載按鈕
    if st.session_state['data_center']:
        st.markdown("### 📥 下載清單：")
        for orig_name, data in st.session_state['data_center'].items():
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"📄 **{data['output_name']}**")
                with c2:
                    st.download_button(
                        label="下載",
                        data=data['content'],
                        file_name=data['output_name'],
                        mime="text/plain",
                        key=f"dl_v74_{orig_name}"
                    )
                st.markdown("---")
else:
    st.warning("尚未偵測到任何檔案上傳。")
