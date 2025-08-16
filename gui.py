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

import streamlit as st
from config.config import my_config, save_config, languages, test_config, \
    delete_first_visit_session_state, app_title
from pages.common import common_ui
from tools.tr_utils import tr

delete_first_visit_session_state("all_first_visit")

common_ui()

st.markdown(f"<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            {app_title}</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>基本配置信息</h2>", unsafe_allow_html=True)

if 'ui_language' not in st.session_state:
    st.session_state['ui_language'] = 'zh-CN - 简体中文'


def set_ui_language():
    print('set_ui_language:', st.session_state['ui_language'])
    my_config['ui']['language'] = st.session_state['ui_language'].split(" - ")[0].strip()
    print('set ui language:', my_config['ui']['language'])
    save_config()




def set_llm_provider():
    my_config['llm']['provider'] = st.session_state['llm_provider']
    save_config()




def set_audio_provider():
    my_config['audio']['provider'] = st.session_state['audio_provider']
    save_config()




def set_audio_key(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['speech_key'] = st.session_state[key]
    save_config()


def set_audio_access_key_id(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['access_key_id'] = st.session_state[key]
    save_config()


def set_audio_access_key_secret(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['access_key_secret'] = st.session_state[key]
    save_config()


def set_audio_app_key(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['app_key'] = st.session_state[key]
    save_config()


def set_audio_region(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['service_region'] = st.session_state[key]
    save_config()


def set_llm_sk(provider, key):
    my_config['llm'][provider]['secret_key'] = st.session_state[key]
    save_config()


def set_llm_key(provider, key):
    my_config['llm'][provider]['api_key'] = st.session_state[key]
    save_config()


def set_llm_base_url(provider, key):
    my_config['llm'][provider]['base_url'] = st.session_state[key]
    save_config()


def set_llm_model_name(provider, key):
    if provider not in my_config['llm']:
        my_config['llm'][provider] = {}
    my_config['llm'][provider]['model_name'] = st.session_state[key]
    save_config()


# 设置language
display_languages = []
selected_index = 0
for i, code in enumerate(languages.keys()):
    display_languages.append(f"{code} - {languages[code]}")
    if f"{code} - {languages[code]}" == st.session_state['ui_language']:
        selected_index = i
# print("selected_index:", selected_index)
selected_language = st.selectbox(tr("Language"), options=display_languages,
                                 index=selected_index, key='ui_language', on_change=set_ui_language)

# 设置语音
audio_container = st.container(border=True)
with audio_container:
    st.info(tr("Audio Provider Info"))

            

    # remote Audio config
    audio_providers = ['Azure', 'Ali', 'Tencent']
    selected_audio_provider = my_config['audio']['provider']
    selected_audio_provider_index = 0
    for i, provider in enumerate(audio_providers):
        if provider == selected_audio_provider:
            selected_audio_provider_index = i
            break

    audio_provider = st.selectbox(tr("Remote Audio Provider"), options=audio_providers,
                                  index=selected_audio_provider_index,
                                  key='audio_provider', on_change=set_audio_provider)
    with st.expander(audio_provider, expanded=True):
        if audio_provider == 'Azure':
            st.info(tr("Audio Azure config"))
            audio_columns = st.columns(2)
            with audio_columns[0]:
                st.text_input(label=tr("Speech Key"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('speech_key', ''),
                              on_change=set_audio_key, key=audio_provider + "_speech_key",
                              args=(audio_provider, audio_provider + '_speech_key'))
            with audio_columns[1]:
                st.text_input(label=tr("Service Region"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('service_region', ''),
                              on_change=set_audio_region,
                              key=audio_provider + "_service_region",
                              args=(audio_provider, audio_provider + '_service_region'))
        if audio_provider == 'Ali':
            st.info(tr("Audio Ali config"))
            audio_columns = st.columns(3)
            with audio_columns[0]:
                st.text_input(label=tr("Access Key ID"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('access_key_id', ''),
                              on_change=set_audio_access_key_id, key=audio_provider + "_access_key_id",
                              args=(audio_provider, audio_provider + '_access_key_id'))
            with audio_columns[1]:
                st.text_input(label=tr("Access Key Secret"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('access_key_secret', ''),
                              on_change=set_audio_access_key_secret, key=audio_provider + "_access_key_secret",
                              args=(audio_provider, audio_provider + '_access_key_secret'))
            with audio_columns[2]:
                st.text_input(label=tr("App Key"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('app_key', ''),
                              on_change=set_audio_app_key, key=audio_provider + "_app_key",
                              args=(audio_provider, audio_provider + '_app_key'))
        if audio_provider == 'Tencent':
            st.info(tr("Audio Tencent config"))
            audio_columns = st.columns(3)
            with audio_columns[0]:
                st.text_input(label=tr("Access Key ID"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('access_key_id', ''),
                              on_change=set_audio_access_key_id, key=audio_provider + "_access_key_id",
                              args=(audio_provider, audio_provider + '_access_key_id'))
            with audio_columns[1]:
                st.text_input(label=tr("Access Key Secret"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('access_key_secret', ''),
                              on_change=set_audio_access_key_secret, key=audio_provider + "_access_key_secret",
                              args=(audio_provider, audio_provider + '_access_key_secret'))
            with audio_columns[2]:
                st.text_input(label=tr("App ID"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('app_key', ''),
                              on_change=set_audio_app_key, key=audio_provider + "_app_key",
                              args=(audio_provider, audio_provider + '_app_key'))

# 设置默认的LLM
llm_container = st.container(border=True)
with (llm_container):
    llm_providers = ['OpenAI', 'Moonshot', 'Azure', 'Qianfan', 'Baichuan', 'Tongyi', 'DeepSeek', 'Ollama']
    saved_llm_provider = my_config['llm']['provider']
    saved_llm_provider_index = 0
    for i, provider in enumerate(llm_providers):
        if provider == saved_llm_provider:
            saved_llm_provider_index = i
            break

    llm_provider = st.selectbox(tr("LLM Provider"), options=llm_providers, index=saved_llm_provider_index,
                                key='llm_provider', on_change=set_llm_provider)
    print(llm_provider)

    # 设置llm的值：
    with st.expander(llm_provider, expanded=True):
        tips = f"""
               ##### {llm_provider} 配置信息
               """
        st.info(tips)
        if llm_provider != 'Ollama':
            st_llm_api_key = st.text_input(tr("API Key"),
                                           value=my_config['llm'].get(llm_provider, {}).get('api_key', ''),
                                           type="password", key=llm_provider + '_api_key', on_change=set_llm_key,
                                           args=(llm_provider, llm_provider + '_api_key'))

        if llm_provider == 'Qianfan':
            st_llm_base_url = st.text_input(tr("Secret Key"),
                                            value=my_config['llm'].get(llm_provider, {}).get('secret_key', ''),
                                            type="password", key=llm_provider + '_secret_key', on_change=set_llm_sk,
                                            args=(llm_provider, llm_provider + '_secret_key'))
        else:
            if llm_provider == 'Azure' or llm_provider == 'DeepSeek' or llm_provider == 'Ollama':
                st_llm_base_url = st.text_input(tr("Base Url"),
                                                value=my_config['llm'].get(llm_provider, {}).get('base_url', ''),
                                                type="password", key=llm_provider + '_base_url',
                                                on_change=set_llm_base_url,
                                                args=(llm_provider, llm_provider + '_base_url'))

        st_llm_model_name = st.text_input(tr("Model Name"),
                                          value=my_config['llm'].get(llm_provider, {}).get('model_name', ''),
                                          key=llm_provider + '_model_name', on_change=set_llm_model_name,
                                          args=(llm_provider, llm_provider + '_model_name'))
