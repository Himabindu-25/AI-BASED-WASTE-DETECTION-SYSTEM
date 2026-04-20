from ultralytics import YOLO
import os

model = YOLO("yolov8n.pt")

# 🔄 Normalize labels
def normalize(label):
    label = label.lower()

    corrections = {
        "vase": "bottle",
        "wine glass": "glass",
        "bowl": "cup",
        "cell phone": "phone",
        "remote": "electronics",
        "tv": "electronics",
        "laptop computer": "laptop",
        "book": "paper",

        # 🔥 Added for toys
        "teddy bear": "toy",
        "doll": "toy",
        "stuffed toy": "toy"
    }

    return corrections.get(label, label)


# 🧠 Keyword Classification (Improved)
def keyword_classify(text):
    text = text.lower()

    if any(k in text for k in [
        "bottle","packet","cover","plastic","bag","wrapper",
        "cup","plate","pen","container"
    ]):
        return "plastic"

    if any(k in text for k in [
        "paper","book","notebook","newspaper","carton","cardboard"
    ]):
        return "paper"

    if any(k in text for k in [
        "can","spoon","knife","metal","steel","scissors","blade","iron"
    ]):
        return "metal"

    if any(k in text for k in ["glass","jar","wine glass"]):
        return "glass"

    if any(k in text for k in [
        "phone","laptop","tv","fan","charger","battery","electronics","remote"
    ]):
        return "e-waste"

    if any(k in text for k in [
        "banana","apple","food","vegetable","fruit","rice"
    ]):
        return "organic"

    if any(k in text for k in [
        "cloth","shirt","doll","dress","fabric","sofa","couch"
    ]):
        return "textile"

    if any(k in text for k in [
        "wood","table","chair","door","furniture"
    ]):
        return "wood"

    return "general"


# ♻️ Category Info (Improved Steps)
def get_info(category):

    mapping = {

    "plastic": ("plastic","🟡 Yellow Bin",[
        "Step 1: Identify plastic type (bottle, wrapper, container)",
        "Step 2: Empty contents and rinse with water",
        "Step 3: Remove caps, labels, and stickers",
        "Step 4: Dry completely to avoid contamination",
        "Step 5: Segregate by plastic type if possible",
        "Step 6: Send to recycling facility for shredding",
        "Step 7: Process into pellets for reuse"
    ]),

    "paper": ("paper","🔵 Blue Bin",[
        "Step 1: Collect paper waste like books, newspapers, cartons",
        "Step 2: Remove plastic covers, pins, and staples",
        "Step 3: Keep paper dry and clean",
        "Step 4: Sort into recyclable categories",
        "Step 5: Send for pulping process",
        "Step 6: Convert pulp into sheets",
        "Step 7: Reuse for printing or packaging"
    ]),

    "metal": ("metal","⚪ Grey Bin",[
        "Step 1: Collect metal items like cans and utensils",
        "Step 2: Clean and remove residues",
        "Step 3: Separate from plastic parts",
        "Step 4: Compress or flatten items",
        "Step 5: Transport to recycling plant",
        "Step 6: Melt metal in furnace",
        "Step 7: Reshape into new products"
    ]),

    "glass": ("glass","🟢 Green Bin",[
        "Step 1: Collect glass bottles carefully",
        "Step 2: Remove caps and lids",
        "Step 3: Clean thoroughly",
        "Step 4: Separate by color",
        "Step 5: Crush into small pieces",
        "Step 6: Melt at high temperature",
        "Step 7: Form new glass items"
    ]),

    "e-waste": ("e-waste","🔴 Red Bin",[
        "Step 1: Identify electronic waste",
        "Step 2: Do not mix with regular waste",
        "Step 3: Backup and erase data",
        "Step 4: Remove batteries",
        "Step 5: Send to certified recycler",
        "Step 6: Extract useful metals",
        "Step 7: Dispose safely"
    ]),

    "organic": ("organic","🟤 Brown Bin",[
        "Step 1: Collect food waste",
        "Step 2: Separate from plastic",
        "Step 3: Put in compost bin",
        "Step 4: Maintain moisture",
        "Step 5: Allow decomposition",
        "Step 6: Convert into compost",
        "Step 7: Use as fertilizer"
    ]),

    "textile": ("textile","🟣 Textile Bin",[
        "Step 1: Collect clothes and fabrics",
        "Step 2: Wash and clean",
        "Step 3: Separate reusable items",
        "Step 4: Donate if usable",
        "Step 5: Shred into fibers",
        "Step 6: Convert into yarn",
        "Step 7: Make new products"
    ]),

    "wood": ("wood","🟫 Wood Waste",[
        "Step 1: Identify wooden items",
        "Step 2: Repair or reuse",
        "Step 3: Remove nails",
        "Step 4: Cut into pieces",
        "Step 5: Process into chips",
        "Step 6: Reuse in furniture",
        "Step 7: Convert into fuel"
    ]),

    "general": ("general","⚫ General Waste",[
        "Step 1: Identify non-recyclable waste",
        "Step 2: Avoid mixing recyclables",
        "Step 3: Dispose properly",
        "Step 4: Transport to landfill",
        "Step 5: Follow safety guidelines"
    ]),
    }

    return mapping.get(category, mapping["general"])


# 🔤 TEXT
def classify_text(text):
    category = keyword_classify(text)
    t,b,s = get_info(category)

    return {
        "type": t,
        "bin": b,
        "steps": s,
        "detected": text
    }


# 📷 IMAGE CLASSIFICATION (FINAL)
def classify_waste(image, filename=None):
    try:
        results = model(image)

        boxes = results[0].boxes
        names = results[0].names

        if boxes is not None and len(boxes) > 0:
            label = names[int(boxes[0].cls[0])]
            conf = float(boxes[0].conf[0])

            label = normalize(label)

            # 🔥 Low confidence handling
            if conf < 0.4:
                label = "unknown"

            # 🔥 Combine label + filename
            combined_text = label
            if filename:
                combined_text += " " + filename.lower()

            category = keyword_classify(combined_text)
            t,b,s = get_info(category)

            return {
                "type": t,
                "bin": b,
                "steps": s,
                "detected": f"{label} ({round(conf,2)})"
            }

    except Exception as e:
        print("YOLO error:", e)

    # 🔥 fallback using filename
    if filename:
        name = os.path.splitext(filename)[0].lower()

        category = keyword_classify(name)
        t,b,s = get_info(category)

        return {
            "type": t,
            "bin": b,
            "steps": s,
            "detected": name
        }

    # 🔥 final fallback
    t,b,s = get_info("general")

    return {
        "type": t,
        "bin": b,
        "steps": s,
        "detected": "unknown item"
    }