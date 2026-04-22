import streamlit as st
import os

st.set_page_config(page_title="SMT 萬用轉檔系統 V8.5", layout="centered")

st.title("🚀 SMT AOI 終極萬用轉檔系統")
st.success("✅ 版本 V8.5：解決欄位偏移問題 (小寫檔專用修正)")

files = st.file_uploader("請上傳 AOI 檔案 (支援多選)", accept_multiple_files=True, key="v85_uploader")

if files:
    st.markdown("---")
    for i, f in enumerate(files):
        try:
            f.seek(0)
            raw_data = f.read()
            
            # 1. 解碼並徹底清除隱形字元
            content = ""
            for enc in ['utf-16', 'gbk', 'utf-8']:
                try:
                    content = raw_data.decode(enc).replace('\x00', '')
                    if len(content) > 10: break
                except: continue

            lines = content.splitlines()
            output_rows = []
            seen = set()
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # 分割欄位 (處理開頭可能是逗號的情況)
                p = [item.strip() for item in line.split(',')]
                
                # --- 智慧定位系統 ---
                d, x, y, a, n = "", "", "", "", ""
                
                # 遍歷所有欄位，找尋「座標符」(如 C1, R10)
                for idx, val in enumerate(p):
                    # 判斷標準：必須是英文字母開頭，後面跟數字 (例如 C12, U5)
                    if val and val[0].isalpha() and any(char.isdigit() for char in val):
                        if "面板" in val or "基准" in val: continue # 跳過基板標記
                        
                        try:
                            # 情況 A：標準格式 (座標符在 [0], X[3], Y[4], 角度[5], 料號[2])
                            if len(p) >= idx + 6 and "." in p[idx+3] and "." in p[idx+4]:
                                d, x, y, a, n = p[idx], p[idx+3], p[idx+4], p[idx+5], p[idx+2]
                            
                            # 情況 B：你提供的小寫檔格式 (座標符在 [idx], 前面是 Z, Y, X)
                            # 根據你提供的資料：[idx-4]=X, [idx-3]=Y, [idx-2]=Angle, [idx+2]=料號
                            elif idx >= 4:
                                d, x, y, a, n = p[idx], p[idx-4], p[idx-3], p[idx-2], p[idx+2]
                            
                            # 驗證座標是否為數字
                            float(x); float(y)
                            
                            if d not in seen and not any(k in d for k in ["参考", "Designator", "類型"]):
                                output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                                seen.add(d)
                                break # 這一行抓到了就跳出
                        except:
                            continue

            # 3. 顯示按鈕
            if output_rows:
                target_name = os.path.splitext(f.name)[0] + ".txt"
                with st.expander(f"✅ 成功轉換：{target_name}", expanded=True):
                    st.download_button(label=f"📥 下載 {target_name}", data="\r\n".join(output_rows), 
                                     file_name=target_name, mime="text/plain", key=f"dl_{i}")
            else:
                st.error(f"❌ 檔案 【{f.name}】 解析失敗，請確認座標欄位位置。")

        except Exception as e:
            st.error(f"❌ 系統錯誤: {e}")
else:
    st.warning("請選取 AOI 檔案上傳。")
