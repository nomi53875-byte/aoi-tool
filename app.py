import streamlit as st
import os

st.set_page_config(page_title="SMT 萬用轉檔工具 V8.3", layout="centered")

st.title("🚀 SMT AOI 終極萬用轉檔系統")
st.success("✅ 版本 V8.3：暴力解碼與字元清洗 (最穩定版本)")

files = st.file_uploader("請上傳 AOI 檔案", accept_multiple_files=True, key="v83_uploader")

if files:
    st.markdown("---")
    for i, f in enumerate(files):
        try:
            f.seek(0)
            raw_bytes = f.read()
            
            # 1. 暴力解碼 (UTF-16 或 GBK)
            try:
                # 針對小寫檔的特殊編碼優先處理
                content = raw_bytes.decode('utf-16', errors='ignore')
                if len(content) < 10 or ' ' not in content: raise Exception
            except:
                content = raw_bytes.decode('gbk', errors='ignore')

            # 2. 核心清洗：把所有不可見字元、空字元強制濾掉
            # 只留下英文字母、數字、逗號、點、換行和常見符號
            clean_content = ""
            valid_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,\n\r\t -_"
            for char in content:
                if char in valid_chars:
                    clean_content += char
                elif char.isprintable(): # 或者是其他可顯示的字元
                    clean_content += char

            lines = clean_content.splitlines()
            output_rows = []
            seen = set()
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # 分割欄位
                p = [item.strip() for item in line.split(',')]
                
                # 為了應付小寫檔前面塞亂碼，我們從後往前找座標
                # 標準格式：座標符在[0], X在[3], Y在[4]...
                # 但如果前面塞了東西，我們找哪一格「看起來像數字」
                try:
                    # 我們嘗試在這一行中尋找連續兩個可以轉成數字的欄位
                    for idx in range(len(p) - 2):
                        try:
                            # 測試當前格 +3, +4 是否為 X, Y 座標
                            d = p[idx]
                            x = p[idx+3]
                            y = p[idx+4]
                            a = p[idx+5]
                            n = p[idx+2]
                            
                            float(x); float(y) # 驗證座標
                            
                            # 座標符必須是英文字母開頭
                            if d and d[0].isalpha() and d not in seen:
                                if not any(k in d for k in ["参考", "Designator", "Part"]):
                                    output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                                    seen.add(d)
                                    break # 這一行抓到正確的就換下一行
                        except:
                            continue
                except:
                    continue

            if output_rows:
                target_name = os.path.splitext(f.name)[0] + ".txt"
                with st.expander(f"✅ 成功轉換：{target_name}", expanded=True):
                    st.download_button(
                        label=f"📥 下載 {target_name}",
                        data="\r\n".join(output_rows),
                        file_name=target_name,
                        mime="text/plain",
                        key=f"dl_v83_{i}_{f.name}"
                    )
            else:
                st.error(f"❌ 檔案 【{f.name}】 解析失敗。")
                with st.expander("查看清洗後的內容 (Debug)"):
                    st.text(clean_content[:500])

        except Exception as e:
            st.error(f"❌ 系統錯誤: {e}")
else:
    st.warning("請選取檔案上傳。")
