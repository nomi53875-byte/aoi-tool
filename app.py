import streamlit as st
import os
import re

st.set_page_config(page_title="SMT 萬用轉檔工具 V8.2", layout="centered")

st.title("🚀 SMT AOI 終極萬用轉檔系統")
st.success("✅ 版本 V8.2：智慧欄位自動對齊 (解決 UTF-16 格式位移)")

files = st.file_uploader("請上傳 AOI 檔案", accept_multiple_files=True, key="v82_uploader")

if files:
    st.markdown("---")
    for i, f in enumerate(files):
        try:
            f.seek(0)
            raw_bytes = f.read()
            
            # 1. 智慧解碼
            content = ""
            if raw_bytes[:2] in [b'\xff\xfe', b'\xfe\xff']:
                content = raw_bytes.decode('utf-16', errors='ignore')
            else:
                try:
                    content = raw_bytes.decode('gbk', errors='ignore')
                except:
                    content = raw_bytes.decode('utf-8', errors='ignore')

            # 2. 深度清洗不可見字元
            content = "".join(char for char in content if char.isprintable() or char in "\n\r\t,")
            lines = content.splitlines()
            output_rows = []
            seen = set()
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # 兼容逗號或 Tab
                p = [item.strip() for item in (line.split(',') if ',' in line else line.split('\t'))]
                
                # 3. 智慧雷達掃描：尋找哪一格是座標符 (例如 R1, C10, U2 等)
                ref_idx = -1
                for idx, val in enumerate(p):
                    # 匹配規則：開頭是字母，後面是數字，長度在 2-10 之間
                    if re.match(r'^[A-Za-z]+\d+[A-Za-z0-9_]*$', val):
                        # 測試這格之後是否能找到看起來像座標的數字 (浮點數)
                        try:
                            # 通常座標在座標符之後的第 3, 4 格，或者是相對位置
                            # 我們在這一行剩下的欄位裡找兩組連續的數字
                            for sub_idx in range(idx + 1, len(p) - 1):
                                float(p[sub_idx])     # 試探 X
                                float(p[sub_idx + 1]) # 試探 Y
                                # 如果成功，這就是我們要的對位點
                                ref_idx = idx
                                x_offset = sub_idx - idx
                                y_offset = sub_idx + 1 - idx
                                angle_offset = sub_idx + 2 - idx if len(p) > sub_idx + 2 else -1
                                part_offset = sub_idx - 1 - idx # 通常料號在座標前一格
                                break
                        except: continue
                    if ref_idx != -1: break

                # 4. 抓取數據
                if ref_idx != -1:
                    try:
                        d = p[ref_idx]
                        x = p[ref_idx + x_offset]
                        y = p[ref_idx + y_offset]
                        a = p[ref_idx + angle_offset] if angle_offset != -1 else "0"
                        n = p[ref_idx + part_offset] if part_offset >= 0 else "Unknown"
                        
                        if d not in seen and not any(k in d for k in ["参考", "Designator", "Part"]):
                            output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)
                    except: continue

            if output_rows:
                target_name = os.path.splitext(f.name)[0] + ".txt"
                with st.expander(f"✅ 成功轉換：{target_name}", expanded=True):
                    st.download_button(
                        label=f"📥 下載 {target_name}",
                        data="\r\n".join(output_rows),
                        file_name=target_name,
                        mime="text/plain",
                        key=f"dl_v82_{i}"
                    )
            else:
                st.error(f"❌ 檔案 【{f.name}】 內容格式無法匹配。")
                with st.expander("查看此檔案清洗後的內容"):
                    st.text(content[:1000])

        except Exception as e:
            st.error(f"❌ 系統錯誤: {e}")
else:
    st.warning("請選取 AOI 檔案上傳。")
