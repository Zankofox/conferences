try:
    # for streamlit >= 1.12.1
    from streamlit.web import bootstrap
except ImportError:
    from streamlit import bootstrap

real_script = 'settings.py'
bootstrap.run(real_script, True, [], {})