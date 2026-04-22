import streamlit as st
import os
import re

st.set_page_config(page_title="SMT 批量轉檔工具 V7.9", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.success("✅ 版本 V7.9：深度清洗模式 (相容所有隱形亂碼)")

files = st.file_uploader("請上傳檔案 (支援多選)", accept_multiple_files=True, key="v79_uploader")

if files:
    st.markdown("---")
    for i, f in enumerate(files):
        try:
            f.seek(0)
            raw_bytes = f.read()
            
            # --- 強力解碼 ---
            content = ""
            try:
                # 處理 UTF-16 BOM
                if raw_bytes[:2] in [b'\xff\xfe', b'\xfe\xff']:
                    content = raw_bytes.decode('utf-16')
                else:
                    content = raw_bytes.decode('gbk', errors='ignore')
            except:
                content = raw_bytes.decode('utf-8', errors='ignore')

            # --- 深度清洗：移除所有 \x00 和奇怪的不可見字元 ---
            content = "".join(char for char in content if char.isprintable() or char in "\n\r\t,")
            lines = content.splitlines()
            output_rows = []
            seen = set()
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # 分割欄位
                p = [item.strip() for item in (line.split(',') if ',' in line else line.split('\t'))]
                
                # --- 智慧欄位對齊 (修正小寫檔開頭帶亂碼的問題) ---
                # 我們尋找哪一個欄位長得像座標符 (開頭是字母，後面跟著數字)
                start_idx = -1
                for idx, val in enumerate(p):
                    if re.match(r'^[A-Za-z]+\d+', val):
                        start_idx = idx
                        break
                
                if start_idx != -1 and len(p) >= start_idx + 6:
                    try:
                        # 重新定位座標符、X、Y、角度、料號
                        d = p[start_idx]
                        x = p[start_idx + 3]
                        y = p[start_idx + 4]
                        a = p[start_idx + 5]
                        n = p[start_idx + 2]
                        
                        float(x); float(y) # 驗證座標
                        
                        if d not in seen and not any(k in d for k in ["参考号", "Designator"]):
                            output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)
                    except: continue

            if not output_rows:
                st.warning(f"⚠️ 檔案 【{f.name}】 仍解析不到有效座標。")
                with st.expander("查看清洗後的內容偵錯"):
                    st.text(content[:1000])
            else:
                target = os.path.splitext(f.name)[0] + ".txt"
                with st.expander(f"✅ 轉換成功：{target}", expanded=True):
                    st.download_button(
                        label=f"📥 下載 {target}",
                        data="\r\n".join(output_rows),
                        file_name=target,
                        mime="text/plain",
                        key=f"dl_v79_{i}"
                    )
        except Exception as e:
            st.error(f"❌ 檔案 {f.name} 發生錯誤: {e}")
