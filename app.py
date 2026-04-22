import streamlit as st
import os

st.set_page_config(page_title="SMT 批量轉檔工具 V7.8", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.success("✅ 版本 V7.8：終極編碼修復 (支援 UTF-16 BOM)")

files = st.file_uploader("請上傳檔案 (支援多選)", accept_multiple_files=True, key="v78_uploader")

if files:
    st.markdown("---")
    for i, f in enumerate(files):
        try:
            f.seek(0)
            raw_bytes = f.read()
            
            # --- 強力解碼邏輯 ---
            content = ""
            # 優先嘗試帶有 BOM 的 UTF-16 (處理 \xff\xfe)
            try:
                content = raw_bytes.decode('utf-16-le' if raw_bytes[:2] == b'\xff\xfe' else 'utf-16')
            except:
                try:
                    content = raw_bytes.decode('gbk', errors='ignore')
                except:
                    content = raw_bytes.decode('utf-8', errors='ignore')

            # 徹底清除隱形字元與空字元
            content = content.replace('\x00', '').strip()
            lines = content.splitlines()
            output_rows = []
            seen = set()
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # 兼容多種分割符號 (逗號或 Tab)
                p = [item.strip() for item in (line.split(',') if ',' in line else line.split('\t'))]
                if len(p) < 6: continue
                
                try:
                    # 座標符[0], X[3], Y[4], 角度[5], 料號[2]
                    d, x, y, a, n = p[0], p[3], p[4], p[5], p[2]
                    float(x); float(y)
                    if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                        if d not in seen and "基准" not in line:
                            output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)
                except: continue

            if not output_rows:
                st.warning(f"⚠️ 檔案 【{f.name}】 內容讀取成功但無有效座標，請檢查格式。")
                with st.expander("查看原始內容偵錯"):
                    st.text(content[:500])
            else:
                target = os.path.splitext(f.name)[0] + ".txt"
                with st.expander(f"✅ 轉換成功：{target}", expanded=True):
                    st.download_button(
                        label=f"📥 下載 {target}",
                        data="\r\n".join(output_rows),
                        file_name=target,
                        mime="text/plain",
                        key=f"dl_v78_{i}_{f.name}"
                    )
        except Exception as e:
            st.error(f"❌ 檔案 {f.name} 發生錯誤: {e}")
