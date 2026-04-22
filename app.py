import streamlit as st
import os

st.set_page_config(page_title="SMT 萬用轉檔系統 V8.4", layout="centered")

st.title("🚀 SMT AOI 終極萬用轉檔系統")
st.info("✅ 版本 V8.4：深度透視模式 (解析失敗將顯示原始內容)")

files = st.file_uploader("請上傳 AOI 檔案", accept_multiple_files=True, key="v84_uploader")

if files:
    st.markdown("---")
    for i, f in enumerate(files):
        try:
            f.seek(0)
            raw_data = f.read()
            
            # 1. 嘗試三種主流編碼，並徹底清除 \x00
            content = ""
            for encoding in ['utf-16', 'gbk', 'utf-8']:
                try:
                    content = raw_data.decode(encoding).replace('\x00', '')
                    if len(content) > 10: break
                except: continue

            lines = content.splitlines()
            output_rows = []
            seen = set()
            
            # 2. 核心解析邏輯
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # 兼容 逗號、Tab、空格 分割
                p = [item.strip() for item in line.replace('\t', ',').replace(' ', ',').split(',') if item.strip()]
                
                # 滑動窗口搜索：尋找符合 (座標符, ?, ?, X, Y, Angle) 特徵的區塊
                for idx in range(len(p) - 5):
                    try:
                        d = p[idx]     # 座標符 (如 C1)
                        x = p[idx+3]   # X 座標
                        y = p[idx+4]   # Y 座標
                        a = p[idx+5]   # 角度
                        n = p[idx+2]   # 料號 (通常在座標符後兩格)
                        
                        # 嚴格驗證：座標必須是數字，座標符必須是字母開頭
                        if d[0].isalpha() and float(x) and float(y):
                            if d not in seen and not any(k in d for k in ["参考", "Designator", "Part"]):
                                output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                                seen.add(d)
                                break
                    except: continue

            # 3. 輸出結果
            if output_rows:
                target_name = os.path.splitext(f.name)[0] + ".txt"
                with st.expander(f"✅ 成功轉換：{target_name}", expanded=True):
                    st.download_button(label="📥 下載 TXT", data="\r\n".join(output_rows), 
                                     file_name=target_name, mime="text/plain", key=f"dl_{i}")
            else:
                st.error(f"❌ 檔案 【{f.name}】 解析失敗")
                # --- 這是最重要的 Debug 資訊 ---
                st.warning("🔍 以下為檔案前 10 行內容，請截圖給我看，我來分析座標位置：")
                st.code("\n".join(lines[:10]))

        except Exception as e:
            st.error(f"❌ 處理 {f.name} 時發生錯誤: {e}")
