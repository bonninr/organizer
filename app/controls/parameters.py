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
import console_parameters


return_variables={}
def make_parameter_controls(organ_type):
    parameters=console_parameters.organ_types[organ_type]
    for category, parameters in parameters.items():
        cols = st.columns(len(parameters))
        for col, parameter in zip(cols, parameters):
            for key, value in parameter.items():
                name = key.replace('_', ' ').capitalize()
                min_value = value * 0.5
                max_value = value * 1.5
                with col:
                    return_variables[key] = st.number_input(name, min_value=min_value, value=float(value), max_value=max_value, step=1.0)
    return return_variables