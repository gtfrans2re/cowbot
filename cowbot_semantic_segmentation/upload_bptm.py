from roboflow import Roboflow
import os

API_KEY = os.getenv("ROBOFLOW_API_KEY")
WORKSPACE = "gtfrans2re"
PROJECT_ID = "cowbot-obstacles-segmentation"

MODEL_TYPE = "yolov11n-seg"
MODEL_PATH = "./weights"   # folder containing best.pt
MODEL_NAME = "cowbot-obstacles-segmentation-bpt-model"


if not API_KEY:
    raise RuntimeError("ROBOFLOW_API_KEY not set")

rf = Roboflow(api_key=API_KEY)

workspace = rf.workspace(WORKSPACE)

print("🚀 Uploading model (workspace-level)...")

workspace.deploy_model(
    model_type=MODEL_TYPE,
    model_path=MODEL_PATH,
    model_name=MODEL_NAME,
    project_ids=[PROJECT_ID],
)

print("Upload complete")
