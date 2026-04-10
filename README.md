# 3D Reconstruction Pipeline from AMtown02 Images to Final Gaussian Splatting Result

<h2>🔥 Step 1: Prepare Input Images</h2>

Input:
AMtown02_extracted/images/

Description:
Original images extracted from dataset.

Select subset:
~/real_images

Reason:
- improve stability
- reduce computation
- better reconstruction

Rules:
- continuous sequence
- good overlap
- low blur
- stable motion


<h2>🔥 Step 2: Create COLMAP Workspace</h2>

Command:
mkdir -p ~/colmap_projects/amtown02_stride2/sparse

Description:
Create working directory for COLMAP


<h2>🔥 Step 3: Feature Extraction</h2>

Command:
colmap feature_extractor \
    --database_path ~/colmap_projects/amtown02_stride2/database.db \
    --image_path ~/real_images

Explanation:
Extract image features → stored in database.db


<h2>🔥 Step 4: Sequential Matching</h2>

Command:
colmap sequential_matcher \
    --database_path ~/colmap_projects/amtown02_stride2/database.db

Explanation:
Match images based on sequence order (video-style data)


<h2>🔥 Step 5: Sparse Reconstruction (SfM)</h2>

Command:
colmap mapper \
    --database_path ~/colmap_projects/amtown02_stride2/database.db \
    --image_path ~/real_images \
    --output_path ~/colmap_projects/amtown02_stride2/sparse

Explanation:
- estimate camera poses
- reconstruct sparse 3D points


<h2>🔥 Step 6: COLMAP Output</h2>

Structure:

```text
~/colmap_projects/amtown02_stride2/
├── database.db
└── sparse/0/
    ├── cameras.bin
    ├── images.bin
    └── points3D.bin
```

Key files:
cameras.bin → intrinsics  
images.bin → poses  
points3D.bin → 3D points  


<h2>🔥 Step 7: Compress Data</h2>

Command:
zip -r real_images.zip real_images/
zip -r colmap_project.zip amtown02_stride2/

Important:
DO NOT compress only sparse/0  
Must include database.db  


<h2>🔥 Step 8: Upload to Google Drive</h2>

Path:
MyDrive/aae5302/

Files:
real_images.zip  
colmap_project.zip  


<h2>🔥 Step 9: Mount Drive</h2>

Command:
from google.colab import drive
drive.mount('/content/drive')


<h2>🔥 Step 10: Unzip Data</h2>

Command:
mkdir -p /content/data
unzip -q "/content/drive/MyDrive/aae5302/real_images.zip" -d /content/data/
unzip -q "/content/drive/MyDrive/aae5302/colmap_project.zip" -d /content/data/

Check:
/content/data/real_images  
/content/data/amtown02_stride2  


<h2>🔥 Step 11: Enable GPU</h2>

Command:
nvidia-smi

Expected:
Tesla T4 GPU  


<h2>🔥 Step 12: Install Dependencies</h2>

Command:
apt-get update
apt-get install -y git cmake build-essential libgl1-mesa-dev
pip install torch torchvision torchaudio  


<h2>🔥 Step 13: Build OpenSplat</h2>

Command:
cd /content
git clone https://github.com/pierotofy/OpenSplat.git
cd OpenSplat
mkdir build
cd build
cmake .. -DTorch_DIR=/usr/local/lib/python3.12/dist-packages/torch/share/cmake/Torch
make -j8  

Important:
Torch path must be correct  


<h2>🔥 Step 14: Run Training</h2>

Command:
/content/OpenSplat/build/opensplat \
/content/data/amtown02_stride2 \
--colmap-image-path /content/data/real_images \
--num-iters 7000 \
--save-every 500 \
--downscale-factor 2  

Key parameters:
--num-iters → training length  
--save-every → save interval  
--downscale-factor → reduce memory usage  


<h2>🔥 Step 15: Training Process</h2>

Logs:
Loading ...  
Step 1000 ...  
Added gaussians  
Culled gaussians  

Meaning:
Model is optimizing scene representation  


<h2>🔥 Step 16: Output Files</h2>

Command:
find /content -name "splat*.ply"

Example:
splat_1000.ply  
splat_4000.ply  
splat_4500.ply  


<h2>🔥 Step 17: Save Results</h2>

Command:
cp /content/splat_*.ply /content/drive/MyDrive/aae5302/


<h2>🔥 Step 18: Visualization</h2>

Download:
Google Drive → MyDrive/aae5302/

Open:
CloudCompare

Usage:
rotate → adjust point size → screenshot → PPT  


<h2>🔥 Final Summary</h2>

Pipeline:

Images  
→ COLMAP feature extraction  
→ image matching  
→ sparse reconstruction  
→ OpenSplat training  
→ splat_xxxx.ply  
→ visualization  


✔ Key Idea:
COLMAP estimates camera poses  
OpenSplat performs neural rendering

## ⚠️ Key Challenges

### ❌ 1. Colab Session Killed During Training (OOM / Timeout)

**Issue:**
Training process stopped around step ~4500 unexpectedly.

**Reason:**
- GPU / RAM memory limit exceeded
- Free Colab session timeout
- Too many Gaussians generated during training
**Solution:**
- Reduce total iterations:
```bash
--num-iters 4500
```

## 🎯 Final Result (Gaussian Splatting)
https://drive.google.com/file/d/1p8sJBuPs_YzKYoyYnDZKb_qGUx1Fr5Mp/view?usp=drive_link
This is the reconstructed 3D scene from the AMtown02 dataset using OpenSplat.

![result](./splat_AMtown02-image.png)

### Observations

- The overall structure of buildings and roads is successfully reconstructed
- RGB colors are preserved from input images
- Some noise and blur exist due to limited iterations and data sampling
