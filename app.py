import streamlit as st
import os

# 設定網頁標題
st.set_page_config(page_title="SMT 批量轉檔工具 V6.3", layout="centered")

st.title("🚀 SMT AOI 批量獨立轉檔系統")
st.success("✅ 版本 V6.3：修正下載後按鈕消失的問題")

# 允許多檔案上傳
uploaded_files = st.file_uploader("請拖曳多個 AOI 檔案進去", type=['aoi'], accept_multiple_files=True)

if uploaded_files:
    st.markdown("### 📥 轉換清單 (請逐一解鎖下載)：")
    
    # 建立一個容器來固定住按鈕
    with st.container():
        for uploaded_file in uploaded_files:
            try:
                # 1. 處理檔名
                base_name = os.path.splitext(uploaded_file.name)[0]
                output_filename = f"{base_name}.txt"

                # 2. 讀取並轉換內容
                content = uploaded_file.read().decode('gbk', errors='ignore')
                lines = content.splitlines()
                output_rows = []
                seen = set()
                
                for line in lines:
                    if not line.strip(): continue
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) < 6: continue
                    
                    try:
                        d, x, y, a, n = parts[0], parts[3], parts[4], parts[5], parts[2]
                        float(x); float(y)
                    except:
                        try:
                            d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                            float(x)
                        except: continue

                    if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                        if d not in seen and "基准" not in line:
                            output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                            seen.add(d)

                if output_rows:
                    final_result = "\r\n".join(output_rows)
                    
                    # 3. 介面優化：使用 columns 讓按鈕對齊
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.info(f"📄 {output_filename} (已就緒)")
                    with c2:
                        # 使用檔案名稱作為 key，避免下載後狀態跑掉
                        st.download_button(
                            label="點我下載",
                            data=final_result,
                            file_name=output_filename,
                            mime="text/plain",
                            key=f"dl_{output_filename}"
                        )
            except Exception as e:
                st.error(f"檔案 {uploaded_file.name} 出錯: {e}")
    
    st.warning("💡 提示：下載一個檔案後，若按鈕消失，請稍微等待或重新移動滑鼠，清單會自動回來。")
