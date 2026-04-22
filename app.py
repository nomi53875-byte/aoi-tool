import streamlit as st
import os
import re

st.set_page_config(page_title="SMT 萬用轉檔工具 V8.0", layout="centered")

st.title("🚀 SMT AOI 究極萬用轉檔系統")
st.success("✅ 版本 V8.0：全自動雷達掃描 (相容所有隱形亂碼與編碼)")

files = st.file_uploader("請選取多個檔案 (不限大小寫)", accept_multiple_files=True, key="v80_uploader")

if files:
    st.markdown("---")
    for i, f in enumerate(files):
        try:
            f.seek(0)
            raw_bytes = f.read()
            
            # --- 強力智慧解碼 ---
            content = ""
            # 優先處理帶有 BOM 的 UTF-16
            if raw_bytes[:2] in [b'\xff\xfe', b'\xfe\xff']:
                content = raw_bytes.decode('utf-16', errors='ignore')
            else:
                # 嘗試 GBK, 若失敗則 UTF-8
                try:
                    content = raw_bytes.decode('gbk', errors='ignore')
                except:
                    content = raw_bytes.decode('utf-8', errors='ignore')

            # 深度清洗：只保留可列印字元與必要的分隔符號
            content = "".join(char for char in content if char.isprintable() or char in "\n\r\t,")
            lines = content.splitlines()
            output_rows = []
            seen = set()
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # 兼容多種分割符
                p = [item.strip() for item in (line.split(',') if ',' in line else line.split('\t'))]
                
                # --- 雷達掃描邏輯：在該行中搜尋真正的座標符位置 ---
                target_idx = -1
                for idx, val in enumerate(p):
                    # 搜尋符合「字母+數字」且長度適中的座標符 (如 C1, R123, U5)
                    if re.match(r'^[A-Za-z]{1,3}\d+[A-Za-z0-9_]*$', val):
                        # 進一步確認後三格是否為數字座標 (X, Y)
                        try:
                            if len(p) >= idx + 5:
                                float(p[idx + 3]) # X
                                float(p[idx + 4]) # Y
                                target_idx = idx
                                break
                        except: continue
                
                # 若找到起始點，抓取數據
                if target_idx != -1:
                    try:
                        d = p[target_idx]      # 座標符
                        x = p[target_idx + 3]  # X
                        y = p[target_idx + 4]  # Y
                        a = p[target_idx + 5]  # 角度
                        n = p[target_idx + 2]  # 料號
                        
                        if d not in seen and not any(k in d for k in ["参考", "Designator"]):
                            output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)
                    except: continue

            if output_rows:
                target_name = os.path.splitext(f.name)[0] + ".txt"
                with st.expander(f"✅ 成功轉換：{target_name}", expanded=True):
                    st.download_button(
                        label=f"📥 點我下載 {target_name}",
                        data="\r\n".join(output_rows),
                        file_name=target_name,
                        mime="text/plain",
                        key=f"final_v80_{i}"
                    )
            else:
                st.error(f"❌ 檔案 【{f.name}】 仍無法解析。請確認內容是否包含座標資料。")

        except Exception as e:
            st.error(f"❌ 檔案 {f.name} 系統報錯: {e}")
else:
    st.warning("請選取 AOI 檔案上傳。")
