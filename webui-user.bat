@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS=--skip-torch-cuda-test --opt-sdp-attention --medvram --no-half-vae --api

call webui.bat
