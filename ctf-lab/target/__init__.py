"""CTF target application package.

Intentionally does not import the Flask app here, so modules like flags.py can
be imported without Flask installed. Import the app explicitly:

    from target.app import create_target_app
"""
