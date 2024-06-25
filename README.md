# AI_DJ_Project

## Downloading Allin1
 
[https://github.com/mir-aidj/all-in-one?tab=readme-ov-file#usage-for-python](https://github.com/mir-aidj/all-in-one?tab=readme-ov-file#usage-for-python)

### 1. Install PyTorch

Visit [PyTorch](https://pytorch.org/) and install the appropriate version for your system.

### 2. Install NATTEN (Required for Linux and Windows; macOS will auto-install)

* **Linux**: Download from [NATTEN website](https://www.shi-labs.com/natten/)
* **macOS**: Auto-installs with `allin1`.
* **Windows**: Build from source:
  
```shell
pip install ninja # Recommended, not required
git clone https://github.com/SHI-Labs/NATTEN
cd NATTEN
make
```

### 3. Install the package

```shell
pip install git+https://github.com/CPJKU/madmom  # install the latest madmom directly from GitHub
pip install allin1  # install this package
```

### 4. (Optional) Install FFmpeg for MP3 support

For ubuntu:

```shell
sudo apt install ffmpeg
```

For macOS:

```shell
brew install ffmpeg
```