import streamlit as st

st.set_page_config(page_title="SMT 工具 V5.0", layout="centered")

st.title("🚀 SMT AOI 萬用轉檔工具")
st.success("✅ 版本 V5.0：純淨下載模式已啟動，下方絕無清單。")

uploaded_file = st.file_uploader("選擇 AOI 檔案", type=['aoi'])

if uploaded_file is not None:
    try:
        content = uploaded_file.read().decode('gbk', errors='ignore')
        lines = content.splitlines()
        output_rows = []
        seen = set()
        
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) >= 6:
                try:
                    # 格式 A
                    d, x, y, a, n = parts[0].strip(), parts[3].strip(), parts[4].strip(), parts[5].strip(), parts[2].strip()
                    float(x), float(y)
                except:
                    try:
                        # 格式 B
                        d, x, y, a, n = parts[5].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[7].strip()
                        float(x), float(y)
                    except: continue

                if d and not any(k in d for k in ["参考号", "库", "標示符", "Designator"]):
                    if d not in seen and "基准" not in line:
                        output_rows.append(f"{d}\t{x}\t{y}\t{a}\tT\t{n}")
                        seen.add(d)

        if output_rows:
            st.info(f"✅ 解析完成：{len(output_rows)} 個零件")
            st.download_button("📥 點此下載 TXT", "\r\n".join(output_rows), f"{uploaded_file.name.split('.')[0]}.txt", use_container_width=True)
        else:
            st.warning("找不到資料")
    except Exception as e:
        st.error(f"錯誤: {e}")