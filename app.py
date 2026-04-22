import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V7.0", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.success("✅ 版本 V7.0：引入狀態鎖定技術，解決檔案覆寫問題")

# 1. 初始化狀態儲存空間 (如果不存在就建立)
if 'file_results' not in st.session_state:
    st.session_state['file_results'] = {}

# 2. 檔案上傳
uploaded_files = st.file_uploader("請【一次框選】多個檔案上傳", type=['aoi'], accept_multiple_files=True)

# 當檔案發生變動時，清空舊狀態重新處理
if uploaded_files:
    st.session_state['file_results'] = {} # 重置，確保不留舊資料
    
    for f in uploaded_files:
        try:
            # 讀取並轉換
            f.seek(0)
            content = f.read().decode('gbk', errors='ignore')
            lines = content.splitlines()
            
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
                # 將結果鎖進狀態儲存空間，Key 加上檔案大小確保唯一性
                fname = os.path.splitext(f.name)[0] + ".txt"
                st.session_state['file_results'][fname] = "\r\n".join(output)
        except Exception as e:
            st.error(f"檔案 {f.name} 處理失敗")

# 3. 從狀態儲存空間把所有按鈕畫出來
if st.session_state['file_results']:
    st.info(f"📊 狀態鎖定成功！已確認處理 {len(st.session_state['file_results'])} 個獨立檔案")
    st.markdown("---")
    
    # 按照字母順序排列按鈕，避免跳動
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
                    key=f"lock_{name}" # 唯一金鑰
                )
            st.markdown("---")
else:
    if uploaded_files:
        st.warning("檔案讀取中或格式不符，請確認是否為正確的 AOI 檔案。")
