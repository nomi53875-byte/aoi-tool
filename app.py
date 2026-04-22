import streamlit as st
import os

# 設定網頁
st.set_page_config(page_title="SMT 工具 V5.3", layout="centered")

st.title("🚀 SMT AOI 萬用轉檔工具")
st.success("✅ 版本 V5.3：檔案名稱同步 + 精確 Tab 格式")

uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        # 1. 自動抓取原始檔名並改為 .txt
        base_name = os.path.splitext(uploaded_file.name)[0]
        output_filename = f"{base_name}.txt"

        # 2. 讀取內容
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        
        output_rows = []
        seen = set()
        
        for line in lines:
            if not line.strip(): continue
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) < 6: continue
            
            # 初始化
            d, x, y, a, n = "", "", "", "", ""
            
            try:
                # 根據 CLG078-219AFA.txt 的排列反推抓取邏輯
                # 假設原始 AOI：parts[0]=座標符, parts[3]=X, parts[4]=Y, parts[5]=角度, parts[2]=料號
                d, x, y, a, n = parts[0], parts[3], parts[4], parts[5], parts[2]
                float(x); float(y) # 驗證數字
            except:
                try:
                    # 備用抓取邏輯
                    d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                    float(x)
                except:
                    continue

            # 過濾與去重
            if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                if d not in seen and "基准" not in line:
                    # 3. 嚴格執行 [TAB] 分隔格式
                    output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                    seen.add(d)

        if output_rows:
            final_content = "\n".join(output_rows)
            
            st.markdown(f"**預期輸出的檔名：** `{output_filename}`")
            
            # 4. 下載按鈕：帶入動態檔名
            st.download_button(
                label=f"📥 點我下載 {output_filename}",
                data=final_content,
                file_name=output_filename,
                mime="text/plain"
            )
            st.info(f"💡 轉換完成！已比照標準格式處理共 {len(output_rows)} 筆。")
            
    except Exception as e:
        st.error(f"發生錯誤：{e}")
