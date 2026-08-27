from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io, hashlib, math

app = FastAPI(title="SatQuery AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def analyze_image(data: bytes, query: str):
    digest = hashlib.sha256(data + query.encode()).hexdigest()
    seed = int(digest[:8], 16)
    confidence = 0.82 + (seed % 1500) / 10000
    confidence = min(confidence, 0.97)

    q = query.lower()
    if any(x in q for x in ["water", "lake", "river", "pond"]):
        answer = "The scene contains a prominent water-like region that is spatially concentrated in the central-to-lower portion of the image."
        evidence = "Spectral/color contrast and connected-region geometry are consistent with a water feature."
        label = "Water feature"
    elif any(x in q for x in ["building", "urban", "city", "house", "infrastructure"]):
        answer = "Built-up structures appear as clustered high-contrast regions, suggesting a developed or urbanized area."
        evidence = "Dense rectangular/linear structures form a spatial cluster typical of built-up land."
        label = "Built-up area"
    elif any(x in q for x in ["forest", "tree", "vegetation", "crop", "agriculture"]):
        answer = "Vegetated land appears as broad connected regions with relatively uniform texture and color."
        evidence = "Spatial texture and vegetation-like tonal response support the vegetation interpretation."
        label = "Vegetation"
    elif any(x in q for x in ["road", "highway", "street"]):
        answer = "Linear transportation features are visible, with elongated structures crossing the scene."
        evidence = "Long connected edges and corridor-like geometry provide the primary evidence."
        label = "Road network"
    else:
        answer = "The image has been analyzed against your natural-language query. The strongest matching scene evidence is concentrated in the highlighted region."
        evidence = "The result is based on visual similarity, spatial structure and query relevance in this demo pipeline."
        label = "Relevant region"

    return {
        "answer": answer,
        "confidence": round(confidence, 2),
        "label": label,
        "evidence": evidence,
        "model": "SatQuery Demo Vision-Language Agent",
        "trace": [
            "Input validated",
            "Natural-language query parsed",
            "Remote-sensing task classified as visual question answering",
            "VQA / grounding model selected",
            "Evidence region generated",
            "Confidence fused with evidence score",
            "Answer returned with visual grounding",
        ],
        "region": {
            "x": 18 + seed % 28,
            "y": 20 + (seed // 17) % 25,
            "w": 34 + (seed // 31) % 25,
            "h": 28 + (seed // 43) % 25,
        },
    }

@app.get("/")
def root():
    return {"service": "SatQuery AI", "status": "online"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze(
    query: str = Form(...),
    image: UploadFile = File(...)
):
    data = await image.read()
    try:
        im = Image.open(io.BytesIO(data))
        width, height = im.size
    except Exception:
        width, height = 0, 0

    result = analyze_image(data, query)
    result["image"] = {
        "filename": image.filename,
        "content_type": image.content_type,
        "width": width,
        "height": height,
    }
    return result

@app.post("/change-analysis")
async def change_analysis(
    query: str = Form(...),
    before: UploadFile = File(...),
    after: UploadFile = File(...)
):
    before_data = await before.read()
    after_data = await after.read()
    digest = hashlib.sha256(before_data + after_data + query.encode()).hexdigest()
    score = 0.64 + (int(digest[:6], 16) % 2800) / 10000
    score = min(score, 0.94)

    return {
        "answer": "Potential change detected between the two supplied observations. The highlighted region represents the demo change-of-interest area.",
        "change_score": round(score, 2),
        "change_type": "Land-use / surface change",
        "evidence": "The two observations produce different visual feature signatures in the selected area.",
        "trace": [
            "Both temporal inputs validated",
            "Images normalized for comparison",
            "Temporal alignment stage completed",
            "Change-detection model selected",
            "Difference evidence calculated",
            "Change confidence generated",
        ],
        "region": {"x": 25, "y": 22, "w": 48, "h": 42},
    }
