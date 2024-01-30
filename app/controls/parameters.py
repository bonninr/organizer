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

import streamlit as st

def make_parameter_controls():
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.number_input("Length",min_value=1.0,value=25.0,step=1.0)
    with col2:
        width = st.number_input("Width",min_value=1.0,value=4.0,step=1.0)
    with col3:
        height = st.number_input("height",min_value=1.0, value=75.0,step=1.0)

    col1, col2, col3 = st.columns(3)
    with col1:
        rail_width = st.number_input("Rail width",min_value=1.0,value=2.0, step=1.0)
    with col2:
        rung_height = st.number_input("Rung Height",min_value=0.1,value=2.0, step=1.0)
    with col3:
        rung_width = st.number_input("Rung Width",min_value=1.0,value=2.0, step=1.0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        rung_padding = st.number_input("Rung Padding",min_value=0.0,value=6.0, step=1.0)

    return {
        'length':length,
        'width':width,
        'height':height,
        'rail_width':rail_width,
        'rung_height':rung_height,
        'rung_width':rung_width,
        'rung_padding':rung_padding
    }