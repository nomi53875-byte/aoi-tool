import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V7.3", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.success("✅ 版本 V7.3：強制相容所有副檔名格式")

# 1. 這裡不設定 type，讓所有檔案都能選取，避免大小寫過濾問題
files = st.file_uploader("請選取多個檔案 (不限大小寫)", accept_multiple_files=True, key="universal_uploader")

# 2. 初始化狀態儲存區
if 'final_store' not in st.session_state:
    st.session_state['final_store'] = {}

if files:
    # 清空前一次的紀錄
    st.session_state['final_store'] = {}
    
    for f in files:
        # 取得副檔名並轉小寫判斷
        ext = os.path.splitext(f.name)[1].lower()
        
        # 只處理副檔名是 .aoi 的檔案 (不管原始是大寫還是小寫)
        if ext == '.aoi':
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
                        d, x, y, a, n = p[0], p[3], p[4], p[5], p[2]
                        float(x); float(y)
                        if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                            if d not in seen and "基准" not in line:
                                output.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                                seen.add(d)
                    except: continue
                
                if output:
                    # 輸出統一存為 .txt
                    new_name = os.path.splitext(f.name)[0] + ".txt"
                    st.session_state['final_store'][f.name] = {
                        "display_name": new_name,
                        "content": "\r\n".join(output)
                    }
            except Exception as e:
                st.error(f"檔案 {f.name} 處理失敗")
    
    # 顯示結果
    if st.session_state['final_store']:
        st.info(f"📊 已成功識別並轉換 {len(st.session_state['final_store'])} 個 AOI 檔案")
        st.markdown("---")
        
        for original_name, data in st.session_state['final_store'].items():
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"📄 **{data['display_name']}**")
                    st.caption(f"來自原始檔: {original_name}")
                with c2:
                    st.download_button(
                        label="下載 TXT",
                        data=data['content'],
                        file_name=data['display_name'],
                        mime="text/plain",
                        key=f"dl_{original_name}"
                    )
                st.markdown("---")
else:
    # 沒檔案時清空狀態
    st.session_state['final_store'] = {}
    st.warning("請選取檔案上傳。")
