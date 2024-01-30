# Copyright 2024 Rodolfo Bonnin
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

def make_sidebar():
    with st.sidebar:
        st.markdown("![](/app/static/logo.jpg)")
        st.title('Openpipes Organizer: Create your own personalized VPO console')
        st.markdown("By: Rodolfo Bonnin")
        organtype=st.selectbox(
    "Choose the type of console to be created:",
    ("General", "Portative", "Minimalist", "Studio", "Vertical"))
    return organtype