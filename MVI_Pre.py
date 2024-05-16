import streamlit as st
conda activate matplotlib
import matplotlib.pyplot as plt
import numpy as np

# 页面标题
st.markdown("<h2 style='font-size: 28px; font-weight: bold; '>Microvascular Invasion (MVI) Risk Assessment</h2>", unsafe_allow_html=True)

# 用户输入肿瘤大小
tumor_size_input = st.text_input('Tumor size (cm)')

# 创建AFP的下拉选择框
afp_input = st.selectbox(
    'AFP (μg/L)',
    ['Select', '≥400', '<400']
)

# 创建肿瘤边缘的下拉选择框
tumor_margin_input = st.selectbox(
    'Tumor margin',
    ['Select', 'non-smooth', 'smooth']
)

# 计算得分的函数
def calculate_scores(tumor_size, afp_choice, tumor_margin_choice):
    tumor_size_score = tumor_size * 2 if tumor_size else 0
    afp_score = 7 if afp_choice == '≥400' else 0
    tumor_margin_score = 14 if tumor_margin_choice == 'non-smooth' else 0
    return tumor_size_score, afp_score, tumor_margin_score

# 检查用户输入并计算得分
if tumor_size_input:
    tumor_size = float(tumor_size_input)  # 将输入转换为浮点数
    tumor_size_score, afp_score, tumor_margin_score = calculate_scores(tumor_size, afp_input, tumor_margin_input)
    total_score = tumor_size_score + afp_score + tumor_margin_score
else:
    st.error("Please enter the Tumor size.")
    total_score = None

# 预测按钮
if st.button('Predict') and total_score is not None:
    # 使用公式计算预测值
    y = 1 / (1 + np.exp(-0.0996078903249369 * total_score + 2.34587192628574))
    
    # 输出预测结果
    st.markdown(f"""<div style='font-family: "Century Gothic", sans-serif; font-weight: bold; font-style: italic; font-size: 1em;'>
     Based on the entered feature values, the predicted possibility of MVI is {y*100:.2f}%.
     </div>""", unsafe_allow_html=True)
    
    # 创建一个matplotlib图表
    plt.figure(figsize=(8, 0.5))  # 定义图表的大小
    plt.barh(['MVI possibility'], [y], color='red')  # 创建水平条形图
    plt.xlim(0.0, 1.0)  # 设置x轴的显示范围从0.0到1.0
    st.pyplot(plt)
else:
    if total_score is None:
        st.write("Please fill in all the fields and click 'Predict' to see the result.")
