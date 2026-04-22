import streamlit as st

# 設定網頁標題與布局
st.set_page_config(page_title="SMT 工具 V5.2", layout="centered")

st.title("🚀 SMT AOI 萬用轉檔工具")
st.success("✅ 版本 V5.2：格式與檔名最終修正版")

uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        # 讀取檔案，使用 GBK 編碼以支援中文
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        
        output_rows = []
        seen = set()
        
        for line in lines:
            if not line.strip(): continue
            # 清除空格並以逗號分割
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) < 6: continue
            
            d, x, y, a, n = "", "", "", "", ""
            
            # --- 核心邏輯：精確抓取欄位 ---
            # 根據你提供的錯誤檔案反推，修正後的對齊邏輯如下：
            try:
                # 判斷座標符、X、Y、角度、料號的位置
                # 這裡採用的邏輯：
                # parts[0]: 座標符 (如 C100)
                # parts[3]: X 座標
                # parts[4]: Y 座標
                # parts[5]: 角度
                # parts[2]: 料號 (如 BNG12...)
                
                temp_d = parts[0]
                temp_x = parts[3]
                temp_y = parts[4]
                temp_a = parts[5]
                temp_n = parts[2]
                
                # 驗證 X, Y 是否為數字，若不是則嘗試另一種排列
                float(temp_x)
                float(temp_y)
                d, x, y, a, n = temp_d, temp_x, temp_y, temp_a, temp_n
            except:
                try:
                    # 備用格式：部分 AOI 座標在 [1],[2]，料號在 [7]，座標符在 [5]
                    d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                    float(x)
                except:
                    continue

            # 排除標題列與重複項
            if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                if d not in seen and "基准" not in line:
                    # 輸出格式：座標符 [TAB] X [TAB] Y [TAB] 角度 [TAB] T [TAB] 料號
                    output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                    seen.add(d)

        if output_rows:
            result_text = "\n".join(output_rows)
            # 點擊按鈕直接下載正確格式的檔案
            st.download_button(
                label="📥 點我下載轉檔後的座標檔 (Coordinate_Fixed.txt)",
                data=result_text,
                file_name="Coordinate_Fixed.txt",
                mime="text/plain"
            )
            st.info(f"💡 處理完成！共轉換 {len(output_rows)} 筆數據。")
            
    except Exception as e:
        st.error(f"轉換發生錯誤：{e}")
