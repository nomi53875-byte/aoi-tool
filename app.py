import streamlit as st

# 設定網頁
st.set_page_config(page_title="SMT 工具 V5.1", layout="centered")

st.title("🚀 SMT AOI 萬用轉檔工具")
st.success("✅ 版本 V5.1：修正欄位對齊與檔名")

uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        # 讀取檔案，強制使用 GBK 解碼（對應 AOI 常見格式）
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        
        output_rows = []
        seen = set()
        
        for line in lines:
            if not line.strip(): continue
            parts = [p.strip() for p in line.split(',')]
            
            # 初始化變數
            d, x, y, a, n = "", "", "", "", ""
            
            # --- 核心邏輯修正：根據你上傳的錯誤檔案反推原始格式 ---
            try:
                if len(parts) >= 8:
                    # 這是針對你原始 AOI 的精確欄位抓取
                    # 假設原始格式中：parts[0]=座標符, parts[3]=X, parts[4]=Y, parts[5]=角度, parts[2]=料號
                    d, x, y, a, n = parts[0], parts[3], parts[4], parts[5], parts[2]
                    
                    # 檢查 X, Y 是否為有效數字，不是的話就嘗試另一種格式
                    float(x)
                    float(y)
                else:
                    continue
            except:
                try:
                    # 備用格式：如果上述失敗，嘗試另一種常見排列
                    if len(parts) >= 8:
                        d, x, y, a, n = parts[5], parts[1], parts[2], parts[3], parts[7]
                        float(x)
                except:
                    continue

            # 過濾掉標題列與重複的座標符
            if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator", "Part"]):
                if d not in seen and "基准" not in line:
                    # 嚴格輸出：座標符 [TAB] X [TAB] Y [TAB] 角度 [TAB] T [TAB] 料號
                    output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                    seen.add(d)

        if output_rows:
            result_text = "\n".join(output_rows)
            # 這裡設定正確的下載檔名
            st.download_button(
                label="📥 點我下載轉檔後的座標檔 (.txt)",
                data=result_text,
                file_name="Coordinate_Fixed.txt",
                mime="text/plain"
            )
            st.info(f"💡 轉換完成，共計 {len(output_rows)} 筆。")
            
    except Exception as e:
        st.error(f"轉換發生錯誤：{e}")
