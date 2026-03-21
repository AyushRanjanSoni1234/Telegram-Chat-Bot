# -----------------------
# Lazy Loader for Vision Models
# -----------------------
_vision_cache = {
    "device": None,
    "processor": None,
    "model": None,
    "reader": None
}

def load_vision():
    """Lazily loads models only when needed."""
    if _vision_cache["model"] is not None:
        return _vision_cache

    import torch
    import easyocr
    from transformers import BlipProcessor, BlipForConditionalGeneration

    # 🔥 Detect if we are using mocked modules (Python 3.14 workaround)
    if hasattr(torch, "_mock_return_value") or "MagicMock" in str(type(torch)):
        raise RuntimeError("PyTorch is currently unvailable (mocked) on this environment.")
    if hasattr(easyocr, "_mock_return_value") or "MagicMock" in str(type(easyocr)):
        raise RuntimeError("EasyOCR is currently unavailable (mocked) on this environment.")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    model.to(device)
    model.eval()

    reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

    _vision_cache.update({
        "device": device,
        "processor": processor,
        "model": model,
        "reader": reader
    })
    return _vision_cache

# -----------------------
# OCR Function
# -----------------------
def extract_text(image_path: str) -> str:
    vision = load_vision()
    result = vision["reader"].readtext(image_path, detail=0)
    text = " ".join(result)
    return text.strip()

# -----------------------
# Caption Function
# -----------------------
def generate_caption(image_path: str) -> str:
    from PIL import Image
    import torch
    
    vision = load_vision()
    image = Image.open(image_path).convert("RGB")

    # safer tensor handling
    inputs = vision["processor"](images=image, return_tensors="pt")
    inputs = {k: v.to(vision["device"]) for k, v in inputs.items()}

    with torch.no_grad():
        output = vision["model"].generate(**inputs)

    caption = vision["processor"].decode(output[0], skip_special_tokens=True)
    return caption.strip()

# -----------------------
# Auto Decision Function
# -----------------------
def process_image(image_path: str) -> dict:
    text = extract_text(image_path)

    # 🔥 better decision logic
    if len(text.split()) > 5:
        return {
            "type": "OCR",
            "output": text
        }
    else:
        caption = generate_caption(image_path)
        return {
            "type": "Caption",
            "output": caption
        }