# app.py
# 主界面：Streamlit 应用
import streamlit as st
import pandas as pd
import numpy as np
from fuzzy_core import inference, TIME_CENTERS
import db, viz, fuzzy_core
from datetime import datetime
import matplotlib.pyplot as plt
import io

# 初始化 DB
db.init_db()

st.set_page_config(page_title="Fuzzy Washer Control System", layout="wide")

st.title("洗衣机洗涤时间模糊推理控制系统")

# 左栏：输入与控制
with st.sidebar:
    st.header("输入控制")
    sludge = st.slider("污泥程度 (0~1)", 0.0, 1.0, 0.5, 0.01)
    grease = st.slider("油脂程度 (0~1)", 0.0, 1.0, 0.5, 0.01)
    engine = st.selectbox("推理引擎", ['mamdani','sugeno'])
    antecedent = st.selectbox("前件合成（仅Mamdani）", ['maxmin','maxprod'])
    defuzz = st.selectbox("去模糊方法（Mamdani）", ['centroid','max'])
    do_save = st.checkbox("自动保存结果到数据库", value=True)
    if st.button("运行推理"):
        if engine == 'sugeno':
            val, label, debug = inference(sludge, grease, engine='sugeno')
            algorithm = 'sugeno'
            defuzz_method = 'sugeno_wa'
        else:
            val, label, debug = inference(sludge, grease, engine='mamdani', antecedent=antecedent, defuzz=defuzz)
            algorithm = f'mamdani_{antecedent}'
            defuzz_method = defuzz
        st.session_state['last_result'] = {'sludge':sludge, 'grease':grease, 'algorithm':algorithm, 'defuzz':defuzz_method, 'result_time':val, 'linguistic':label, 'created_at': datetime.utcnow().isoformat() }
        st.success(f"推理完成：时间={val:.3f}，语言描述={label}")
        if do_save:
            db.insert_record(sludge, grease, algorithm, defuzz_method, val, label)

# 中间：结果与算法对比
st.subheader("推理结果与算法对比")
col1, col2 = st.columns([1,1])
with col1:
    # show last result
    last = st.session_state.get('last_result', None)
    if last:
        st.markdown("**上次运行结果：**")
        st.write(last)
    else:
        st.info("请在左侧输入参数并点击“运行推理”来生成结果。")
with col2:
    st.markdown("**多算法对比（同一输入下）**")
    if st.button("运行所有算法比较（当前滑块值）"):
        results = []
        inputs = {'sludge':sludge, 'grease':grease}
        # mamdani maxmin centroid
        v1, l1, _ = inference(sludge, grease, engine='mamdani', antecedent='maxmin', defuzz='centroid')
        v2, l2, _ = inference(sludge, grease, engine='mamdani', antecedent='maxprod', defuzz='centroid')
        v3, l3, _ = inference(sludge, grease, engine='mamdani', antecedent='maxmin', defuzz='max')
        v4, l4, _ = inference(sludge, grease, engine='sugeno')
        results = [
            ('mamdani_maxmin_centroid', v1, l1),
            ('mamdani_maxprod_centroid', v2, l2),
            ('mamdani_maxmin_max', v3, l3),
            ('sugeno', v4, l4)
        ]
        df_cmp = pd.DataFrame(results, columns=['algorithm','value','label'])
        st.table(df_cmp)
        # save comparisons into DB as separate records if desired
        if st.checkbox("将比较结果保存为历史记录", value=False):
            for alg, val, lab in results:
                db.insert_record(sludge, grease, alg, 'compare', float(val), lab)

# 右侧：可视化 & 隶属函数
st.subheader("可视化：隶属函数 / 推理平面 / 历史趋势")
viz_tab1, viz_tab2, viz_tab3 = st.tabs(["隶属函数", "3D 推理平面", "历史趋势"])

with viz_tab1:
    fig = viz.plot_membership_functions()
    st.pyplot(fig)

with viz_tab2:
    fig3d = viz.plot_3d_surface(engine=engine, antecedent=antecedent, defuzz=defuzz, res=41)
    st.pyplot(fig3d)

with viz_tab3:
    rows = db.query_all(limit=500)
    df = pd.DataFrame(rows, columns=['id','sludge','grease','algorithm','defuzz','result_time','linguistic','created_at'])
    if df.empty:
        st.info("暂无历史记录")
    else:
        fig_hist = viz.plot_history_stats(df)
        st.pyplot(fig_hist)
        st.dataframe(df)

# 历史记录管理区
st.subheader("历史记录管理（增/删/改/查）")
rows = db.query_all(limit=500)
df = pd.DataFrame(rows, columns=['id','sludge','grease','algorithm','defuzz','result_time','linguistic','created_at'])
st.dataframe(df)

col_del, col_mod = st.columns(2)
with col_del:
    del_id = st.number_input("删除记录 ID（填写上表 id）", min_value=0, value=0, step=1)
    if st.button("删除记录"):
        if del_id > 0:
            db.delete_record(int(del_id))
            st.success("删除成功")
        else:
            st.warning("请填写有效 id")

with col_mod:
    st.markdown("修改记录（输入id并填写新值）")
    mod_id = st.number_input("修改记录 id", min_value=0, value=0, step=1, key='modid')
    m_sludge = st.number_input("污泥 new", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    m_grease = st.number_input("油脂 new", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    m_algorithm = st.selectbox("算法 new", ['mamdani_maxmin','mamdani_maxprod','sugeno'])
    m_defuzz = st.selectbox("defuzz new", ['centroid','max','sugeno_wa'])
    if st.button("提交修改"):
        if mod_id > 0:
            # recompute value based on chosen alg
            if m_algorithm.startswith('sugeno'):
                val, lab, _ = inference(m_sludge, m_grease, engine='sugeno')
            else:
                ant = 'maxmin'
                if 'maxprod' in m_algorithm: ant='maxprod'
                val, lab, _ = inference(m_sludge, m_grease, engine='mamdani', antecedent=ant, defuzz=m_defuzz)
            db.update_record(int(mod_id), m_sludge, m_grease, m_algorithm, m_defuzz, float(val), lab)
            st.success("修改并更新成功")
        else:
            st.warning("请填写有效 id")

# 导出历史记录为 CSV
if st.button("导出历史记录为 CSV"):
    rows = db.query_all(limit=10000)
    df = pd.DataFrame(rows, columns=['id','sludge','grease','algorithm','defuzz','result_time','linguistic','created_at'])
    csv = df.to_csv(index=False)
    st.download_button("点击下载 CSV", csv, file_name='fuzzy_history.csv', mime='text/csv')

st.markdown("---")
st.caption("工程级实现：fuzzy_core.py (核心算法) | db.py (DB CRUD) | viz.py (可视化) | app.py (Streamlit GUI)")
