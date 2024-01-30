# Copyright 2023 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#--------------------  

import streamlit as st
from controls import (
    make_sidebar, 
    make_parameter_controls, 
    make_model_controls,
    make_file_controls
)

def __make_ui():
    tab1, tab2 = st.tabs(["Parameters", "File"])
    with tab1:
        col1, col2, col3 = st.columns(3)
        model_parameters = make_parameter_controls()

    with tab2:
        file_controls = make_file_controls()

    _, col2, _= st.columns(3)
    with col2:
        color1 = st.color_picker('Primary Color', '#E0BD00')
    
    if 'key'not in st.session_state:
        st.session_state['key'] = 0
    else:
        st.session_state['key'] = 1

    if st.button('Generate Model', type="primary") or st.session_state['key']==0:
        
        make_model_controls(
            model_parameters,
            color1, 
            file_controls
        )
    else:
        st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬆️Please click the \"Generate Model\" Button")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Organizer - VPO console plans creator",
        page_icon="🧊"
    )

    #st.title('CadQuery Box Test')
    __make_ui()
    make_sidebar()