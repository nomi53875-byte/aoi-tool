import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 批量轉檔工具 V7.5", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.success("✅ 版本 V7.5：解決大小寫顯示衝突問題")

# 1. 萬用上傳
files = st.file_uploader("請選取多個檔案 (不限大小寫)", accept_multiple_files=True, key="v75_uploader")

if files:
    st.info(f"📊 系統偵測到檔案總數：{len(files)} 個")
    st.markdown("---")
    
    # 建立一個清單來存放轉換後的結果
    final_list = []

    for f in files:
        try:
            f.seek(0)
            raw = f.read().decode('gbk', errors='ignore')
            lines = raw.splitlines()
            
            output_rows = []
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
                            output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)
                except: continue
            
            # 只要有內容，就存進清單 (不管檔名大小寫)
            if output_rows:
                final_list.append({
                    "orig_name": f.name,
                    "target_name": os.path.splitext(f.name)[0] + ".txt",
                    "content": "\r\n".join(output_rows)
                })
        except Exception as e:
            st.error(f"檔案 {f.name} 解析失敗")

    # 2. 依照清單順序，強迫畫出所有按鈕
    if final_list:
        st.markdown("### 📥 下載清單：")
        for i, item in enumerate(final_list):
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    # 這裡同時顯示原始檔名，方便你確認大小寫
                    st.write(f"📄 **{item['target_name']}**")
                    st.caption(f"來源：{item['orig_name']}")
                with c2:
                    # 使用 i (序號) 作為 key，這是最保險的做法
                    st.download_button(
                        label="下載",
                        data=item['content'],
                        file_name=item['target_name'],
                        mime="text/plain",
                        key=f"download_idx_{i}" 
                    )
                st.markdown("---")
else:
    st.warning("請選取檔案上傳。")
