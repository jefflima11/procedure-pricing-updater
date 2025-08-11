import streamlit as st

def state_function(function):
        if function['type'] == 'S':
            st.success(function['msg'], icon="✅")
        else:
            st.warning(function['msg'], icon="⚠️")