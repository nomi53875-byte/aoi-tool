import streamlit as st
import os

st.set_page_config(page_title="SMT 批量轉檔工具 V7.7", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.success("✅ 版本 V7.7：支援 UTF-16 編碼 (解決小寫檔解析失敗問題)")

files = st.file_uploader("請上傳檔案 (支援多選)", accept_multiple_files=True, key="v77_uploader")

if files:
    st.markdown("---")
    for i, f in enumerate(files):
        try:
            f.seek(0)
            raw_bytes = f.read()
            
            # --- 智慧解碼邏輯 ---
            content = ""
            # 優先嘗試 UTF-16 (為了解決截圖中出現 \x00 的問題)
            try:
                content = raw_bytes.decode('utf-16')
                if '\x00' in content or len(content) < 10: # 如果讀出來還是怪怪的
                    raise ValueError
            except:
                # 備援方案：嘗試 GBK 或 UTF-8
                try:
                    content = raw_bytes.decode('gbk', errors='ignore')
                except:
                    content = raw_bytes.decode('utf-8', errors='ignore')

            lines = content.splitlines()
            output_rows = []
            seen = set()
            
            for line in lines:
                # 去除隱形的空字元並處理分割
                line = line.replace('\x00', '').strip()
                if not line: continue
                
                p = [item.strip() for item in line.split(',')]
                if len(p) < 6: continue
                
                try:
                    d, x, y, a, n = p[0], p[3], p[4], p[5], p[2]
                    float(x); float(y) # 驗證座標
                    if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                        if d not in seen and "基准" not in line:
                            output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)
                except: continue

            if not output_rows:
                st.warning(f"⚠️ 檔案 【{f.name}】 解析不到座標。請確認內部格式。")
            else:
                target = os.path.splitext(f.name)[0] + ".txt"
                with st.expander(f"✅ 轉換成功：{target}", expanded=True):
                    st.download_button(
                        label=f"📥 下載 {target}",
                        data="\r\n".join(output_rows),
                        file_name=target,
                        mime="text/plain",
                        key=f"dl_v77_{i}_{f.name}"
                    )
        except Exception as e:
            st.error(f"❌ 檔案 {f.name} 發生錯誤: {e}")
