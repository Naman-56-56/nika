
import os, cv2, numpy as np, torch, math
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from skimage.measure import perimeter
from skimage.feature import graycomatrix, graycoprops
from sklearn.metrics.pairwise import cosine_similarity

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL = None
MASK_GEN = None

def load_model_once(checkpoint="sam_vit_h.pth", model_type="vit_h"):
    global MODEL, MASK_GEN
    if MODEL is None:
        MODEL = sam_model_registry[model_type](checkpoint=checkpoint).to(DEVICE)
        MASK_GEN = SamAutomaticMaskGenerator(MODEL)
    return MASK_GEN

def run_sam_on_image(img_path, max_masks=50):
    mask_gen = load_model_once()
    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    masks = mask_gen.generate(img_rgb)
    return masks

def metrics_dashboard(img_path, masks, refs=None, max_masks=10):
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    H, W, _ = img.shape
    outputs = []
    for i, m in enumerate(masks[:max_masks]):
        seg = m['segmentation']
        if seg.sum() == 0: continue

        # area ratio
        area_ratio = seg.sum() / (H * W)

        # compactness
        try:
            per = perimeter(seg, neighborhood=8)
            comp = (4 * math.pi * seg.sum()) / (per**2 + 1e-6)
        except Exception:
            comp = 0.0

        # mean color
        mean_color = img[seg].mean(axis=0) / 255.0

        # color similarity
        sim_scores = {}
        if refs:
            for name, ref_rgb in refs.items():
                sim = cosine_similarity([mean_color], [ref_rgb])[0,0]
                sim_scores[name] = round(float(sim), 3)

        # texture
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            mask_gray = gray[seg]
            levels = (mask_gray / 32).astype(np.uint8)
            if len(levels) < 2:
                contrast, homogeneity = 0.0, 0.0
            else:
                glcm = graycomatrix(levels.reshape(-1,1),
                                    distances=[1],
                                    angles=[0],
                                    levels=8,
                                    symmetric=True,
                                    normed=True)
                contrast = graycoprops(glcm, 'contrast')[0,0]
                homogeneity = graycoprops(glcm, 'homogeneity')[0,0]
        except Exception:
            contrast, homogeneity = 0.0, 0.0

        # anomaly score
        score = (
            min(area_ratio*5, 1.0) * 0.2 +
            min(comp, 1.0) * 0.2 +
            (max(sim_scores.values()) * 0.3 if sim_scores else 0) +
            (contrast / (contrast+5)) * 0.15 +
            homogeneity * 0.15
        )

        outputs.append({
            "id": i,
            "area_%": round(area_ratio*100,2),
            "compactness": round(comp,3),
            "mean_color": [round(c,3) for c in mean_color],
            "color_sims": sim_scores,
            "texture_contrast": round(contrast,3),
            "texture_homogeneity": round(homogeneity,3),
            "anomaly_score": round(score*100,2)
        })
    return outputs

ref_colors = {
    "iron_oxide": np.array([0.7,0.3,0.2]),
    "copper": np.array([0.2,0.6,0.3]),
    "sulfur": np.array([0.9,0.9,0.2])
}
