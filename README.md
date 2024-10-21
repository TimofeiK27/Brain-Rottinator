install imagemagik, select legacy options, add to path
conda install ffmpeg

conda env export > environment.yml to export env
conda env create --file packages.yml to download environment

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if warning about numpy 2.0
    pip uninstall numpy
    pip install numpy==1.26.4

pip install tkvideoplayer

pip install ffpyplayer

25 seconds per image gen

3 min for 7-8 frame video (30 second)
1 min video compilation
30 second upload

5 min per (30 second) video