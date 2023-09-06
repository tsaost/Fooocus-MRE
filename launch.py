import os
import sys
import platform
import fooocus_version

from modules.launch_util import is_installed, run, python, \
    run_pip, repo_dir, git_clone, requirements_met, script_path, dir_repos
from modules.model_loader import load_file_from_url
# from modules.path import modelfile_path, lorafile_path, clip_vision_path, controlnet_path
from modules.path import modelfile_path, lorafile_path

REINSTALL_ALL = False


def prepare_environment():
    torch_index_url = os.environ.get('TORCH_INDEX_URL', "https://download.pytorch.org/whl/cu118")
    torch_command = os.environ.get('TORCH_COMMAND',
                                   f"pip install torch==2.0.1 torchvision==0.15.2 --extra-index-url {torch_index_url}")
    requirements_file = os.environ.get('REQS_FILE', "requirements_versions.txt")

    xformers_package = os.environ.get('XFORMERS_PACKAGE', 'xformers==0.0.21')

    comfy_repo = os.environ.get('COMFY_REPO', "https://github.com/comfyanonymous/ComfyUI")
    comfy_commit_hash = os.environ.get('COMFY_COMMIT_HASH', "62efc78a4b13b87ef0df51323fe1bd71b433fa11")

    print(f"Python {sys.version}")
    print(f"Fooocus version: {fooocus_version.version}")

    comfyui_name = 'ComfyUI-from-StabilityAI-Official'
    git_clone(comfy_repo, repo_dir(comfyui_name), "Inference Engine", comfy_commit_hash)
    sys.path.append(os.path.join(script_path, dir_repos, comfyui_name))

    if REINSTALL_ALL or not is_installed("torch") or not is_installed("torchvision"):
        run(f'"{python}" -m {torch_command}', "Installing torch and torchvision", "Couldn't install torch", live=True)

    if REINSTALL_ALL or not is_installed("xformers"):
        if platform.system() == "Windows":
            if platform.python_version().startswith("3.10"):
                run_pip(f"install -U -I --no-deps {xformers_package}", "xformers", live=True)
            else:
                print("Installation of xformers is not supported in this version of Python.")
                print(
                    "You can also check this and build manually: https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Xformers#building-xformers-on-windows-by-duckness")
                if not is_installed("xformers"):
                    exit(0)
        elif platform.system() == "Linux":
            run_pip(f"install -U -I --no-deps {xformers_package}", "xformers")

    if REINSTALL_ALL or not requirements_met(requirements_file):
        run_pip(f"install -r \"{requirements_file}\"", "requirements")

    return


model_filenames = [
    ('sd_xl_base_1.0_0.9vae.safetensors',
     'https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0_0.9vae.safetensors'),
    ('sd_xl_refiner_1.0_0.9vae.safetensors',
     'https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0_0.9vae.safetensors')
]

lora_filenames = [
    ('sd_xl_offset_example-lora_1.0.safetensors',
     'https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_offset_example-lora_1.0.safetensors')
]

clip_vision_filenames = [
    ('clip_vision_g.safetensors',
     'https://huggingface.co/stabilityai/control-lora/resolve/main/revision/clip_vision_g.safetensors')
]

controlnet_filenames = [
    ('control-lora-canny-rank128.safetensors',
     'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-canny-rank128.safetensors'),
    ('control-lora-canny-rank256.safetensors',
     'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-canny-rank256.safetensors'),
    ('control-lora-depth-rank128.safetensors',
     'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-depth-rank128.safetensors'),
    ('control-lora-depth-rank256.safetensors',
     'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-depth-rank256.safetensors')
]


def download_models():
    for file_name, url in model_filenames:
        load_file_from_url(url=url, model_dir=modelfile_path, file_name=file_name)
    for file_name, url in lora_filenames:
        load_file_from_url(url=url, model_dir=lorafile_path, file_name=file_name)
    for file_name, url in clip_vision_filenames:
        load_file_from_url(url=url, model_dir=clip_vision_path, file_name=file_name)
    for file_name, url in controlnet_filenames:
        load_file_from_url(url=url, model_dir=controlnet_path, file_name=file_name)
    return


def clear_comfy_args():
    argv = sys.argv
    sys.argv = [sys.argv[0]]
    import comfy.cli_args
    sys.argv = argv


def cuda_malloc():
    import cuda_malloc


prepare_environment()

clear_comfy_args()
# cuda_malloc()

# download_models()

from webui import *
