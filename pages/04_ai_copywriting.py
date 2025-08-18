#  Copyright © [2024] 程序那些事
#
#  All rights reserved. This software and associated documentation files (the "Software") are provided for personal and educational use only. Commercial use of the Software is strictly prohibited unless explicit permission is obtained from the author.
#
#  Permission is hereby granted to any person to use, copy, and modify the Software for non-commercial purposes, provided that the following conditions are met:
#
#  1. The original copyright notice and this permission notice must be included in all copies or substantial portions of the Software.
#  2. Modifications, if any, must retain the original copyright information and must not imply that the modified version is an official version of the Software.
#  3. Any distribution of the Software or its modifications must retain the original copyright notice and include this permission notice.
#
#  For commercial use, including but not limited to selling, distributing, or using the Software as part of any commercial product or service, you must obtain explicit authorization from the author.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Author: 程序那些事
#  email: flydean@163.com
#  Website: [www.flydean.com](http://www.flydean.com)
#  GitHub: [https://github.com/ddean2009/MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus)
#
#  All rights reserved.
#
#

import os
import streamlit as st
from datetime import datetime
from langchain_core.prompts import PromptTemplate

from config.config import my_config, app_title
from pages.common import common_ui
from services.llm.llm_provider import get_llm_provider
from tools.tr_utils import tr

common_ui()

st.markdown(f"<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            {app_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align: center;padding-top: 0rem;'>{tr('AI Copywriting')}</h2>", unsafe_allow_html=True)

def read_product_selling_points():
    """读取产品卖点文件"""
    try:
        with open('product_selling_point.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        st.error(f"读取产品卖点文件失败: {e}")
        return ""


# 默认提示词模板
default_prompt = """You are a professional TikTok advertising copywriter. Based on the following product information, create a natural, conversational TikTok advertising video script.

Product Information:
{product_info}

IMPORTANT: Your output must be in the EXACT same format as the example below - a continuous, natural speaking script without any sections, headings, or formatting. 

Example format (DO NOT use any other format):
I've been using it for a few weeks now and I'm obsessed. It's so easy to use. You just apply your toner as usual and then you use the silicone jelly brush to evenly apply a layer of mask. It forms a unique collagen film that acts as a protective barrier, locking in moisture like a fortress. It keeps your skin moisturized and soft throughout the day. It restores skin elasticity and fights sagging and dullness. You can leave it on overnight for best results or wait 15-20 minutes if you're in a hurry. It's so easy to use and it's so effective. I'm gonna link it below if you want to try it out. It's so affordable and it's so worth it. It's gonna make your skin look so much confident and radiant. So, go ahead and buy it now.

Requirements:
1. Write as if someone is speaking naturally to the camera (30-60 seconds of speech)
2. Start with personal experience/testimonial 
3. Explain how to use the product
4. Highlight key benefits and effects
5. End with strong call-to-action
6. Use casual, conversational language with contractions (I'm, it's, you're, etc.)
7. NO sections, headings, bullet points, or formatting - just continuous natural speech
8. Must sound authentic and spontaneous like a real person recommending a product

Generate ONLY the continuous speaking script - nothing else. Please respond in English only."""

# UI界面
st.subheader(tr("AI Copywriting Generator"))

# 读取产品卖点
product_info = read_product_selling_points()

if product_info:
    with st.expander(tr("Product Selling Points"), expanded=False):
        st.text_area(tr("Product Information"), value=product_info, height=200, disabled=True)
else:
    st.warning(tr("Product selling points file not found"))

# 提示词编辑区域
st.subheader(tr("Prompt Template"))
prompt_text = st.text_area(
    tr("Edit Prompt Template"),
    value=default_prompt,
    height=400,
    help=tr("You can modify the prompt template to customize the copywriting style")
)

# 初始化session state用于存储生成的文案
if 'generated_copywriting' not in st.session_state:
    st.session_state.generated_copywriting = ""

# 生成按钮
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_button = st.button(tr("Generate AI Copywriting"), type="primary", use_container_width=True)

# 生成文案
if generate_button:
    # 清空之前的文案内容
    st.session_state.generated_copywriting = ""
    if not product_info:
        st.error(tr("Please ensure product selling points file exists"))
        st.stop()
    
    # 检查LLM配置
    llm_provider = my_config.get('llm', {}).get('provider')
    if not llm_provider:
        st.error(tr("Please configure LLM provider first"))
        st.stop()
    
    try:
        with st.spinner(tr("Generating copywriting...")):
            # 获取LLM服务
            llm_service = get_llm_provider(llm_provider)
            
            # 创建提示词模板
            prompt_template = PromptTemplate.from_template(prompt_text)
            
            # 生成文案
            copywriting_content = llm_service.generate_content(
                topic="",  # 不需要topic，信息在prompt中
                prompt_template=PromptTemplate.from_template(prompt_text.format(product_info=product_info)),
                language="en"  # 使用英文生成
            )
            
            # 将生成的文案保存到session state
            st.session_state.generated_copywriting = copywriting_content
            st.success(tr("Copywriting generated successfully!"))
                
    except Exception as e:
        st.error(f"{tr('Failed to generate copywriting')}: {str(e)}")

# 显示生成的文案区域
st.subheader(tr("Generated Copywriting"))

def update_copywriting():
    """更新文案内容"""
    st.session_state.generated_copywriting = st.session_state.copywriting_editor

copywriting_content = st.text_area(
    tr("Copywriting Content"),
    value=st.session_state.generated_copywriting,
    height=400,
    key="copywriting_editor",
    on_change=update_copywriting,
    placeholder=tr("Generated copywriting will appear here and you can edit it...")
)

