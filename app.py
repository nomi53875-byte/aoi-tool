import streamlit as st
import os

st.set_page_config(page_title="SMT 批量轉檔工具 V7.6", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.info("✅ 版本 V7.6：內容深度診斷模式")

files = st.file_uploader("請上傳檔案", accept_multiple_files=True, key="v76_uploader")

if files:
    st.markdown("---")
    for i, f in enumerate(files):
        try:
            f.seek(0)
            raw_bytes = f.read()
            # 診斷：如果檔案太小，直接報錯
            if len(raw_bytes) < 100:
                st.error(f"❌ 檔案 【{f.name}】 太小 ({len(raw_bytes)} bytes)，裡面可能沒有座標資料。")
                continue

            content = raw_bytes.decode('gbk', errors='ignore')
            lines = content.splitlines()
            output_rows = []
            seen = set()
            
            for line in lines:
                if not line.strip(): continue
                p = [item.strip() for item in line.split(',')]
                if len(p) < 6: continue
                try:
                    d, x, y, a, n = p[0], p[3], p[4], p[5], p[2]
                    float(x); float(y)
                    if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                        if d not in seen and "基准" not in line:
                            output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)
                except: continue

            # 如果抓不到座標，顯示原因
            if not output_rows:
                st.warning(f"⚠️ 檔案 【{f.name}】 已讀取，但內容不符合 AOI 座標格式（可能是空檔或加密檔）。")
                # 這裡增加一個小功能：讓你看看檔案前兩行長怎樣，幫忙抓鬼
                st.code(f"檔案前兩行內容：\n{lines[:2]}")
            else:
                target = os.path.splitext(f.name)[0] + ".txt"
                with st.expander(f"✅ 轉換成功：{target}", expanded=True):
                    st.download_button(
                        label=f"📥 下載 {target}",
                        data="\r\n".join(output_rows),
                        file_name=target,
                        mime="text/plain",
                        key=f"dl_final_{i}"
                    )
        except Exception as e:
            st.error(f"❌ 檔案 {f.name} 發生系統錯誤: {e}")
