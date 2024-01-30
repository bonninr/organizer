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
import streamlit.components.v1 as components
import cadquery as cq
from cqterrain import Ladder
import os
import time
import console


EXPORT_NAME = 'model'
PREVIEW_NAME = 'preview.svg'

def __generate_model(parameters):
    model=console.generate_general_console(parameters)
    return model



def __generate_preview_image(model, image_name, color ):
    #create the preview image
    hex_1 = color.lstrip('#')
    rgb_1 = tuple(int(hex_1[i:i+2], 16) for i in (0, 2, 4))

    hex_2 = color.lstrip('#')
    rgb_2 = tuple(int(hex_2[i:i+2], 16) for i in (0, 2, 4))
    cq.exporters.export(model.rotate((0,0,0), (1,0,0), -90), "app/static/prev1.svg", opt={
        "projectionDir": (1, 0.1, 1),
        "showAxes": True,
    })

    cq.exporters.export(model.rotate((0,0,0), (1,0,0), -90).rotate((0,0,0), (0,1,0), -45), "app/static/prev2.svg", opt={
        "projectionDir": (1, 0.1, 1),
        "showAxes": True,
    })

    cq.exporters.export(model.rotate((0,0,0), (1,0,0), -90).rotate((0,0,0), (0,1,0), -90), "app/static/prev3.svg", opt={
        "projectionDir": (1, 0.1, 1),
        "showAxes": True,
    })

def __stl_preview(color):
    # Load and embed the JavaScript file
    with open("js/three.min.js", "r") as js_file:
        three_js = js_file.read()

    with open("js/STLLoader.js", "r") as js_file:
        stl_loader = js_file.read()

    with open("js/OrbitControls.js", "r") as js_file:
        orbital_controls = js_file.read()

    with open("js/stl-viewer.js", "r") as js_file:
        stl_viewer_component = js_file.read().replace('{__REPLACE_COLOR__}',f'0x{color[1:]}')
        


    components.html(
        r'<div style="height:500px">'+
        r'<script>'+
        three_js+' '+
        stl_loader+' '+
        orbital_controls+' '+
        stl_viewer_component+' '+
        r'</script>'+
        r'<stl-viewer model="./app/static/model.stl?cache='+str(time.time())+r'"></stl-viewer>'+
        r'</div>',
        height = 500
    )


def make_model_controls(
    parameters,
    color,
    file_controls
):
    start = time.time()
    with st.spinner('Generating Model..'):
        download_name = file_controls['name']
        export_type = file_controls['type'] 
        model = __generate_model(parameters)

        #create the model file for downloading
        cq.exporters.export(model,f'{EXPORT_NAME}.{export_type}')
        cq.exporters.export(model,'app/static/'+f'{EXPORT_NAME}.stl')
        #__generate_preview_image(model, PREVIEW_NAME, color)
        

        end = time.time()

        #st.write("Preview:")
        __stl_preview(color)
        #st.image(PREVIEW_NAME)

        if f'{EXPORT_NAME}.{export_type}' not in os.listdir():
            st.error('The program was not able to generate the mesh.', icon="🚨")
        else:
            with open(f'{EXPORT_NAME}.{export_type}', "rb") as file:
                btn = st.download_button(
                        label=f"Download {export_type}",
                        data=file,
                        file_name=f'{download_name}.{export_type}',
                        mime=f"model/{export_type}"
                    )
            st.success(f'Rendered in {int(end-start)} seconds', icon="✅")