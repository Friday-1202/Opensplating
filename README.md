# Opensplating
# 3D Reconstruction Pipeline from AMtown02 Images to Final Gaussian Splatting Result

---

<h2>🔥 Step 1: Prepare Input Images</h2>

```text
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

<h2>🔥 Step 2: Create COLMAP Workspace</h2>
